"""
PCX Export File Validation Utilities
"""

from pathlib import Path
from typing import Tuple, List, Dict, Any
import re


class PCXValidator:
    """Validate PCX export file structure"""

    # PCX Schema rules
    REQUIRED_SECTIONS = ['ADD DESTINATION', 'ADD RULE']
    FIELD_WIDTH = 30
    MAX_LINE_LENGTH = 255
    MIN_FILE_SIZE = 100

    @staticmethod
    def validate_file(file_path: Path) -> Tuple[bool, List[str]]:
        """Validate PCX export file structure"""
        errors: List[str] = []

        if not file_path.exists():
            return False, ["File does not exist"]

        # Check file size
        file_size = file_path.stat().st_size
        if file_size < PCXValidator.MIN_FILE_SIZE:
            errors.append(f"File too small: {file_size} bytes")

        with open(file_path, 'r') as f:
            content = f.read()
            lines = content.split('\n')

        # Check for required sections
        for required in PCXValidator.REQUIRED_SECTIONS:
            if required not in content:
                errors.append(f"Missing required section: {required}")

        # Validate line structure
        in_block = False
        line_num = 0

        for line in lines:
            line_num += 1

            # Check line length
            if len(line) > PCXValidator.MAX_LINE_LENGTH:
                errors.append(f"Line {line_num} exceeds max length")

            # Check block structure
            if line.startswith('ADD '):
                in_block = True
                continue

            if in_block and line.strip() and not line.startswith('    '):
                # Non-indented line should be comment or new block
                if not line.startswith('*') and not line.startswith('ADD '):
                    errors.append(
                        f"Line {line_num}: Invalid indentation in block"
                    )

            # Validate key-value format
            if in_block and '=' in line:
                if not re.match(r'^\s{4}\S+\s+=\s+.*$', line):
                    errors.append(f"Line {line_num}: Invalid key-value format")

        return len(errors) == 0, errors

    @staticmethod
    def parse_blocks(file_path: Path) -> List[Dict[str, Any]]:
        """Parse PCX file into blocks"""
        blocks: List[Dict[str, Any]] = []
        current_block = None
        current_fields = {}

        with open(file_path, 'r') as f:
            for line in f:
                line = line.rstrip('\n')

                # Skip comments and empty lines
                if line.startswith('*') or not line.strip():
                    continue

                # New block
                if line.startswith('ADD '):
                    if current_block:
                        blocks.append({
                            'type': current_block,
                            'fields': current_fields
                        })
                    current_block = line[4:].strip()
                    current_fields = {}

                # Field in block
                elif '=' in line and line.startswith('    '):
                    parts = line.split('=', 1)
                    key = parts[0].strip()
                    value = parts[1].strip() if len(parts) > 1 else ''
                    current_fields[key] = value

        # Add last block
        if current_block:
            blocks.append({
                'type': current_block,
                'fields': current_fields
            })

        return blocks
