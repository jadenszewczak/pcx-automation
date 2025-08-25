"""Handle large PCX export files efficiently"""

from pathlib import Path
from typing import Optional, List, Tuple
import re
from datetime import datetime
from utils.formatters import print_success


class LargePCXFileHandler:
    """Efficiently process large PCX export files"""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.file_size_mb = file_path.stat().st_size / (1024 * 1024)

    def find_insertion_point(self, after_section: str = "RULESET") -> int:
        """Find where to insert new content in the file

        Returns byte position to insert at
        """
        print(
            f"Scanning {self.file_size_mb:.1f}MB file for insertion point..."
        )

        last_position = 0
        pattern = f"ADD {after_section}"

        # Read in chunks to handle large file
        chunk_size = 1024 * 1024  # 1MB chunks
        with open(
            self.file_path, 'r', encoding='utf-8', errors='ignore'
        ) as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                # Find last occurrence of pattern
                for match in re.finditer(pattern, chunk):
                    last_position = f.tell() - len(chunk) + match.start()

        # Now find the end of this block
        with open(
            self.file_path, 'r', encoding='utf-8', errors='ignore'
        ) as f:
            f.seek(last_position)
            # Read until we find the next ADD statement or end
            while True:
                line = f.readline()
                if not line or line.strip().startswith('ADD '):
                    return f.tell()

        return last_position

    def backup_file(self) -> Path:
        """Create a backup of the large file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = (
            self.file_path.parent /
            f"{self.file_path.stem}_backup_{timestamp}.txt"
        )

        print(
            f"Creating backup of {self.file_size_mb:.1f}MB file..."
        )
        print("This may take a moment...")

        # Copy in chunks for large files
        chunk_size = 10 * 1024 * 1024  # 10MB chunks
        with open(self.file_path, 'rb') as src:
            with open(backup_path, 'wb') as dst:
                while True:
                    chunk = src.read(chunk_size)
                    if not chunk:
                        break
                    dst.write(chunk)

        print_success(f"Backup created: {backup_path}")
        return backup_path

    def append_content(
        self,
        new_content: str,
        at_position: Optional[int] = None
    ):
        """Append or insert content into the large file"""
        if at_position is None:
            # Simple append at end
            print("Appending content to end of file...")
            with open(self.file_path, 'a', encoding='utf-8') as f:
                f.write('\n\n')
                f.write(new_content)
        else:
            # Insert at specific position - need to rewrite file
            print(f"Inserting content at position {at_position}...")
            temp_file = (
                self.file_path.parent /
                f"{self.file_path.stem}_temp.txt"
            )

            with open(self.file_path, 'rb') as src:
                with open(temp_file, 'wb') as dst:
                    # Copy everything before insertion point
                    dst.write(src.read(at_position))
                    # Write new content
                    dst.write(b'\n\n')
                    dst.write(new_content.encode('utf-8'))
                    dst.write(b'\n\n')
                    # Copy rest of file
                    chunk_size = 10 * 1024 * 1024
                    while True:
                        chunk = src.read(chunk_size)
                        if not chunk:
                            break
                        dst.write(chunk)

            # Replace original with temp
            temp_file.replace(self.file_path)

        print_success("Content added successfully")

    def validate_structure(self) -> Tuple[bool, List[str]]:
        """Quick validation of file structure"""
        issues: List[str] = []

        print(
            f"Validating {self.file_size_mb:.1f}MB file structure..."
        )

        # Check file size
        if self.file_size_mb > 100:
            issues.append(
                f"File very large ({self.file_size_mb:.1f}MB) - "
                "import may be slow"
            )

        required_sections = [
            'ADD DESTINATION',
            'ADD RULE',
            'ADD RULESET'
        ]
        found_sections: set[str] = set()
        found_sections: set[str] = set()

        with open(
            self.file_path, 'r', encoding='utf-8', errors='ignore'
        ) as f:
            for line_num, line in enumerate(f, 1):
                if line_num > 10000:  # Just check first 10k lines
                    break
                for section in required_sections:
                    if section in line:
                        found_sections.add(section)

        for required in required_sections:
            if required not in found_sections:
                issues.append(f"Missing section: {required}")

        return len(issues) == 0, issues
