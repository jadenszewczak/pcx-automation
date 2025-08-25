"""
Tax Report Consolidation Module - EMERGENCY TOOL
Handles consolidated tax reports for multiple companies
"""

from datetime import datetime
from pathlib import Path
from typing import List
import shutil

# Import from your existing modules structure
from modules import BaseModule
from utils.formatters import (
    print_header, print_success, print_error, print_warning
)
from templates.tax_report import TaxReportTemplate


class TaxReportModule(BaseModule):
    """Emergency tax report consolidation tool"""

    def __init__(self):
        super().__init__("Tax Report Consolidation")
        self.backup_dir = Path("data/backups")
        self.backup_dir.mkdir(exist_ok=True, parents=True)

    def display_menu(self):
        """Display tax report menu"""
        print_header(self.name)
        print("\n1. Ticket #231589 - Add Company 147 to existing tax reports")
        print("2. Custom consolidation")
        print("3. Validate export file")
        print("4. Back to main menu")

    def run(self):
        """Run tax report module"""
        while True:
            self.display_menu()
            choice = input("\nSelect an option: ").strip()

            if choice == '1':
                self.process_ticket_231589()
            elif choice == '2':
                self.custom_consolidation()
            elif choice == '3':
                self.validate_file()
            elif choice == '4':
                break
            else:
                print_error("Invalid option.")

    def process_ticket_231589(self):
        """Process ticket #231589 - Add company 147 to tax reports"""
        print_header("Processing Ticket #231589")
        print("\nThis will add Company 147 (DiBrunos)")
        print("to the following tax reports:")

        reports = [
            'TAX001', 'TAX001AD', 'TAX001FF', 'TAX004',
            'TAX010', 'TAX010FD', 'TAX010FT', 'TAX010HA', 'TAX010ST'
        ]

        for report in reports:
            print(f"  • {report}")

        print("\n📁 File Options:")
        print("1. Edit existing PCX export from server")
        print("2. Create new import file")

        choice = input("\nSelect option (1 or 2): ").strip()

        if choice == '1':
            # Work with existing large file
            file_path = input(
                "\nEnter path to PCX export file from server: "
            ).strip()
            file_path = Path(file_path)

            if not file_path.exists():
                print_error("File not found!")
                return

            # Handle large file
            try:
                from utils.large_file_handler import LargePCXFileHandler

                handler = LargePCXFileHandler(file_path)
                print("\n📊 File Info:")
                print(f"   Size: {handler.file_size_mb:.1f} MB")

                # Validate structure
                is_valid, issues = handler.validate_structure()
                if not is_valid:
                    print_warning("⚠️ File validation issues:")
                    for issue in issues:
                        print(f"   - {issue}")
                    if not self.confirm_action("Continue anyway?"):
                        return

                # Create backup
                backup_path = handler.backup_file()

                # Generate new content
                companies = ['147']
                generator = TaxReportTemplate()
                new_content = generator.generate_consolidated(
                    companies, reports
                )

                # Find where to insert (after last RULESET)
                print("\n🔍 Finding insertion point in file...")
                position = handler.find_insertion_point(
                    after_section="RULESET"
                )

                if self.confirm_action(
                    "\n✅ Ready to add Company 147 configuration. Continue?"
                ):
                    # Add the new content
                    handler.append_content(new_content, at_position=position)

                    print_success(
                        "\n✅ Tax report configuration added successfully!"
                    )
                    print(f"📄 Modified file: {file_path}")
                    print(f"💾 Backup saved: {backup_path}")
                    print("\n📋 Next steps:")
                    print("1. Upload modified file back to server")
                    print("2. Import into PCX using Admin → Advanced Import")
                    print("3. Verify Company 147 appears in report breakouts")
                    print("4. Close ticket #231589")

            except ImportError:
                print_warning("Large file handler not available yet.")
                print("For now, using simple append method...")

                # Fallback to simple approach
                backup_path = self.create_backup(file_path)
                companies = ['147']

                if self.generate_consolidated_reports(
                    file_path, companies, reports
                ):
                    print_success("\n✅ Configuration appended to file!")
                    print(f"📄 Modified file: {file_path}")
                    print(f"💾 Backup: {backup_path}")

        elif choice == '2':
            # Create new file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_path = Path(
                f"data/exports/tax_report_147_{timestamp}.txt"
            )
            file_path.parent.mkdir(exist_ok=True, parents=True)

            # Create new file with header
            with open(file_path, 'w') as f:
                f.write("* PCX Export File - Tax Report Configuration\n")
                f.write(f"* Generated: {datetime.now().isoformat()}\n")
                f.write("* Ticket: #231589\n")
                f.write("* Purpose: Add Company 147 to tax reports\n\n")

            print_success(f"Created new file: {file_path}")

            companies = ['147']

            if self.confirm_action(
                "\nGenerate configuration for Company 147?"
            ):
                if self.generate_consolidated_reports(
                    file_path, companies, reports
                ):
                    print_success("\n✅ Configuration file created!")
                    print(f"📄 File: {file_path}")
                    print("\n📋 Import this file into PCX to complete ticket")

    def process_ticket_231589_quick(self):
        """Quick processing for emergency ticket - called from CLI"""
        print_header("EMERGENCY: Processing Ticket #231589")
        print("Adding Company 147 (DiBrunos) to tax reports...")

        # Use default path for quick mode
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = Path(
            f"data/exports/tax_147_quick_{timestamp}.txt"
        )
        file_path.parent.mkdir(exist_ok=True, parents=True)

        # Create file with header
        with open(file_path, 'w') as f:
            f.write("* Quick Generation - Ticket #231589\n\n")

        companies = ['147']
        reports = [
            'TAX001', 'TAX001AD', 'TAX001FF', 'TAX004',
            'TAX010', 'TAX010FD', 'TAX010FT', 'TAX010HA', 'TAX010ST'
        ]

        success = self.generate_consolidated_reports(
            file_path, companies, reports
        )

        if success:
            print_success(f"\n✅ Configuration generated: {file_path}")
            print("\n📋 Import this file into PCX to complete ticket #231589")
        else:
            print_error("Failed to generate configuration")

    def create_backup(self, file_path: Path) -> Path:
        """Create timestamped backup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = (
            self.backup_dir /
            f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
        )
        shutil.copy2(file_path, backup_path)
        print_success(f"Backup created: {backup_path}")
        return backup_path

    def generate_consolidated_reports(
        self, file_path: Path,
        companies: List[str],
        reports: List[str]
    ) -> bool:
        """Generate the actual consolidated reports"""
        try:
            generator = TaxReportTemplate()
            new_content = generator.generate_consolidated(
                companies, reports
            )

            # Append to file
            with open(file_path, 'a') as f:
                f.write(new_content)

            # Print summary
            print("\n📊 Generated configuration for:")
            print(f"   • Companies: {', '.join(companies)}")
            print(f"   • Reports: {len(reports)} tax reports")

            return True

        except Exception as e:
            print_error(f"Generation failed: {str(e)}")
            return False

    def custom_consolidation(self):
        """Custom consolidation setup"""
        print_header("Custom Tax Report Consolidation")

        # Get company numbers
        companies_input = input(
            "Enter company numbers (comma-separated): "
        ).strip()
        if not companies_input:
            print_warning("No companies specified")
            return

        companies = [c.strip() for c in companies_input.split(',')]

        # Get report names
        print("\nEnter report names (one per line, blank to finish):")
        reports: List[str] = []
        while True:
            report = input("> ").strip().upper()
            if not report:
                break
            reports.append(report)

        if not reports:
            print_warning("No reports specified")
            return

        # Generate configuration
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = Path(
            f"data/exports/custom_tax_{timestamp}.txt"
        )
        file_path.parent.mkdir(exist_ok=True, parents=True)

        with open(file_path, 'w') as f:
            f.write("* Custom Tax Report Configuration\n")
            f.write(f"* Companies: {', '.join(companies)}\n\n")

        if self.generate_consolidated_reports(
            file_path, companies, reports
        ):
            print_success(f"\n✅ Custom configuration saved to: {file_path}")

    def validate_file(self):
        """Validate PCX export file"""
        print_header("Validate Export File")
        file_path = input("Enter file path: ").strip()

        if not Path(file_path).exists():
            print_error("File not found!")
            return

        # Basic validation
        with open(file_path, 'r') as f:
            content = f.read()

        checks = {
            'Has ADD RULE blocks': 'ADD RULE' in content,
            'Has RULESETNAME': 'RULESETNAME' in content,
            'Has DESTINATIONNAME': 'DESTINATIONNAME' in content,
            'Has components': 'ADD RULECOMPONENT' in content
        }

        print("\n📋 Validation Results:")
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"  {status} {check}")

        if all(checks.values()):
            print_success("\nFile appears to be valid PCX export format!")
        else:
            print_warning("\nFile may have issues - review before importing")
