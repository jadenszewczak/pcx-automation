"""Fast PCX file editor for large files - stream-based approach"""

from pathlib import Path
from typing import List
import re
from datetime import datetime


class FastPCXEditor:
    """Edit large PCX files without loading into memory"""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.temp_file = file_path.parent / f"{file_path.stem}_temp.txt"

    def find_section_positions(self, section_name: str) -> List[int]:
        """Find all positions where a section starts - FAST"""
        positions: List[int] = []
        pattern = f"^ADD {section_name}"

        with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
            position = 0
            for line in f:
                if re.match(pattern, line):
                    positions.append(position)
                position = f.tell()

        return positions

    def find_last_rule_position(self) -> int:
        """Find where to insert new rules - after last ADD RULE block"""
        last_rule_pos = 0
        in_rule_block = False

        with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
            position = 0
            for line in f:
                if line.startswith('ADD RULE'):
                    in_rule_block = True
                    last_rule_pos = position
                elif (
                    in_rule_block and line.startswith('ADD ')
                    and not line.startswith('ADD RULECOMPONENT')
                ):
                    # We've hit the next section
                    return position
                position = f.tell()

        return last_rule_pos

    def insert_rules_fast(self, new_rules: str) -> bool:
        """Insert new rules at the correct position - FAST"""
        print("Finding insertion point...")
        insert_pos = self.find_last_rule_position()

        print(f"Inserting at position {insert_pos}")

        # Stream copy with insertion
        with open(self.file_path, 'rb') as source:
            with open(self.temp_file, 'wb') as target:
                # Copy everything up to insertion point
                source.seek(0)
                target.write(source.read(insert_pos))

                # Insert new rules
                target.write(b'\n\n')
                target.write(new_rules.encode('utf-8'))
                target.write(b'\n\n')

                # Copy rest of file
                source.seek(insert_pos)
                chunk_size = 10 * 1024 * 1024  # 10MB chunks
                while True:
                    chunk = source.read(chunk_size)
                    if not chunk:
                        break
                    target.write(chunk)

        # Replace original with temp
        backup = (
            self.file_path.parent /
            (
                f"{self.file_path.stem}_backup_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
        )
        self.file_path.rename(backup)
        self.temp_file.rename(self.file_path)

        print(f"✅ Rules inserted! Backup: {backup}")
        return True

    def find_and_modify_rules(
        self, report_names: List[str], company_numbers: List[str]
    ) -> bool:
        """Find specific reports and add company numbers to them"""

        # This would find each report and modify its rule
        # For now, we'll just add new rules

        new_rules: List[str] = []

        for report in report_names:
            for company in company_numbers:
                # Generate a simple rule block
                rule = (
                    "ADD RULE\n"
                    f"    RULESETNAME               = {report}\n"
                    "    SEQUENCE                  = "
                    f"{company}\n"
                    "    DESCRIPTION               = Company "
                    f"{company} added to {report}\n"
                    "    INACTIVE                  = N\n"
                    "    DESTINATIONNAME           = /Reports/"
                    f"{report}~{company}/\n"
                    "    ADD RULECOMPONENT\n"
                    "        VARIABLE              = &RPT_COMPANY\n"
                    "        OPERATOR              = Equal\n"
                    f"        VALUE                 = {company}\n"
                    "        ENDCOMPONENT          = N\n"
                    "    ADD RULECOMPONENT\n"
                    "        VARIABLE              = &RPT_COMPANY\n"
                    "        OPERATOR              = Not Equal\n"
                    f"        VALUE                 = {company}\n"
                    "        ENDCOMPONENT          = Y"
                )
                new_rules.append(rule)

        return self.insert_rules_fast('\n\n'.join(new_rules))
