"""PCX Export File Schema and Structure Manager"""

from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
import re


@dataclass
class PCXSection:
    """Represents a section in the PCX file"""
    name: str
    order: int
    content: List[str]
    start_line: int
    end_line: int


class PCXSchemaManager:
    """Manages PCX export file structure and operations"""

    # Define the canonical section order
    SECTION_ORDER = {
        'PRINTSERVER': 1,
        'RETENTIONPOLICY': 2,
        'INDEXTEMPLATE': 3,
        'INDEXFIELD': 4,
        'TEMPLATELOCATION': 5,
        'DESTINATION': 6,
        'RULESET': 7,
        'RULE': 8,
        'REPORTDEFN': 9,
        'VARIABLE': 10
    }

    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = file_path
        self.sections: Dict[str, PCXSection] = {}
        self.raw_lines: List[str] = []
        if file_path and file_path.exists():
            self.parse_file()

    def parse_file(self) -> None:
        """Parse PCX file into structured sections"""
        if not self.file_path:
            raise ValueError("No file path set")
        with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
            self.raw_lines = f.readlines()
        current_section: Optional[str] = None
        current_content: List[str] = []
        section_start = 0
        for i, line in enumerate(self.raw_lines):
            # Check for new section
            if line.startswith('ADD '):
                # Extract section type
                match = re.match(r'^ADD\s+(\w+)', line)
                if match:
                    section_type = match.group(1)
                    # Save previous section if exists
                    if current_section:
                        self.sections.setdefault(
                            current_section,
                            PCXSection(
                                name=current_section,
                                order=self.SECTION_ORDER.get(
                                    current_section, 99
                                ),
                                content=[],
                                start_line=section_start,
                                end_line=i-1
                            )
                        )
                        self.sections[current_section].content.extend(
                            current_content
                        )
                    # Check if we're continuing the same section type
                    # or starting new
                    if section_type != current_section:
                        current_section = section_type
                        current_content = []
                        section_start = i
            if current_section:
                current_content.append(line)
        # Don't forget the last section
        if current_section:
            self.sections.setdefault(
                current_section,
                PCXSection(
                    name=current_section,
                    order=self.SECTION_ORDER.get(current_section, 99),
                    content=[],
                    start_line=section_start,
                    end_line=len(self.raw_lines)-1
                )
            )
            self.sections[current_section].content.extend(current_content)

    def find_section(self, section_type: str) -> Optional[PCXSection]:
        """Find a specific section in the file"""
        return self.sections.get(section_type)

    def add_to_section(self, section_type: str, content: str) -> bool:
        """Add content to the appropriate section"""
        if section_type not in self.SECTION_ORDER:
            raise ValueError(f"Unknown section type: {section_type}")
        section = self.find_section(section_type)
        if section:
            # Insert at the end of this section
            section.content.append(content + '\n')
            return True
        else:
            # Section doesn't exist, create it in the right order
            self._create_section(section_type, content)
            return True

    def _create_section(self, section_type: str, content: str) -> None:
        """Create a new section in the correct position"""
        target_order = self.SECTION_ORDER[section_type]
        # Create the new section
        new_section = PCXSection(
            name=section_type,
            order=target_order,
            content=[content + '\n'],
            start_line=-1,  # Will be recalculated on save
            end_line=-1
        )
        self.sections[section_type] = new_section

    def delete_from_section(self, section_type: str, identifier: str) -> bool:
        """Delete specific content from a section"""
        section = self.find_section(section_type)
        if not section:
            return False
        # Find and remove the matching block
        new_content: List[str] = []
        skip_block = False
        block_depth = 0
        for line in section.content:
            if identifier in line and line.startswith('ADD '):
                skip_block = True
                block_depth = 0
                continue
            if skip_block:
                # Track nesting depth
                stripped_line = line.strip()
                if stripped_line.startswith('ADD '):
                    block_depth += 1
                elif (
                    not stripped_line
                    or (
                        not line.startswith('    ')
                        and block_depth == 0
                    )
                ):
                    skip_block = False
                if skip_block:
                    continue
            new_content.append(line)
        section.content = new_content
        return True

    def update_in_section(
        self, section_type: str, identifier: str, new_content: str
    ) -> bool:
        """Update specific content in a section"""
        # This is delete + add
        if self.delete_from_section(section_type, identifier):
            return self.add_to_section(section_type, new_content)
        return False

    def save(self, output_path: Optional[Path] = None) -> None:
        """Save the structured content back to file"""
        save_path = output_path or self.file_path
        if not save_path:
            raise ValueError("No output path specified")
        with open(save_path, 'w', encoding='utf-8') as f:
            # Write sections in correct order
            for section_name in sorted(
                self.sections.keys(),
                key=lambda x: self.SECTION_ORDER.get(x, 99)
            ):
                section = self.sections[section_name]
                for line in section.content:
                    f.write(line if line.endswith('\n') else line + '\n')
                f.write('\n')  # Section separator

    def validate_structure(self) -> Tuple[bool, List[str]]:
        """Validate the file structure"""
        issues: List[str] = []
        # Check section order
        prev_order = 0
        for section in sorted(self.sections.values(), key=lambda x: x.order):
            if section.order < prev_order:
                issues.append(f"Section {section.name} is out of order")
            prev_order = section.order
        # Check required sections
        if 'RULE' in self.sections and 'RULESET' not in self.sections:
            issues.append("RULE section exists without RULESET")
        return len(issues) == 0, issues

    def get_statistics(self) -> Dict[str, int]:
        """Get counts of each section type"""
        stats: Dict[str, int] = {}
        for section_name, section in self.sections.items():
            # Count ADD statements in section
            count = sum(
                1 for line in section.content
                if line.startswith(f'ADD {section_name}')
            )
            stats[section_name] = count
        return stats
