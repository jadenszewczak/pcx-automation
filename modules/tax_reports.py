"""
Tax Report Consolidation Module - EMERGENCY TOOL
Handles consolidated tax reports for multiple companies
"""

from datetime import datetime
from pathlib import Path
from typing import List
import shutil
from modules import BaseModule
from utils.formatters import print_header, print_success, print_error


class TaxReportModule(BaseModule):
    """Emergency tax report consolidation tool"""

    def __init__(self):
        super().__init__("Tax Report Consolidation")
        self.backup_dir = Path("data/backups")
        self.backup_dir.mkdir(exist_ok=True)

    def display_menu(self):
        """Display tax report menu"""
        print_header(self.name)
        print("\n1. Ticket #231589 - Companies 120, 121, 147")
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
        """Quick process for ticket #231589"""
        print_header("Processing Ticket #231589")

        file_path = input("Enter PCX export file path: ").strip()
        if not Path(file_path).exists():
            print_error("File not found!")
            return

        # Create backup first
        backup_path = self.create_backup(Path(file_path))
        print_success(f"Backup created: {backup_path}")

        # Generate consolidated configs
        companies = ['120', '121', '147']
        reports = [
            'TAX001', 'TAX001AD', 'TAX001FF', 'TAX004',
            'TAX010', 'TAX010FD', 'TAX010FT', 'TAX010HA', 'TAX010ST'
        ]

        confirm_msg = (
            "Create consolidated reports for companies "
            f"{', '.join(companies)}?"
        )
        if self.confirm_action(confirm_msg):
            success = self.generate_consolidated_reports(
                Path(file_path), companies, reports
            )
            if success:
                print_success("✅ Tax reports configured successfully!")
            else:
                print_error("Failed to generate reports")

    def process_ticket_231589_quick(self):
        """Quick processing for emergency ticket - called from CLI"""
        print_header("EMERGENCY: Processing Ticket #231589")

        file_path = input("Enter PCX export file path: ").strip()
        if not file_path or not Path(file_path).exists():
            print_error("Invalid file path!")
            return

        companies = ['120', '121', '147']
        reports = [
            'TAX001', 'TAX001AD', 'TAX001FF', 'TAX004',
            'TAX010', 'TAX010FD', 'TAX010FT', 'TAX010HA', 'TAX010ST'
        ]

        backup_path = self.create_backup(Path(file_path))
        print_success(f"Backup created: {backup_path}")

        success = self.generate_consolidated_reports(
            Path(file_path), companies, reports
        )

        if success:
            print_success("✅ Tax reports configured successfully!")
        else:
            print_error("Failed to generate reports")

    def create_backup(self, file_path: Path) -> Path:
        """Create timestamped backup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = (
            self.backup_dir /
            f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
        )
        shutil.copy2(file_path, backup_path)
        return backup_path

    def generate_consolidated_reports(
        self, file_path: Path,
        companies: List[str],
        reports: List[str]
    ) -> bool:
        """Generate the actual consolidated reports"""
        from templates.tax_report import TaxReportTemplate

        generator = TaxReportTemplate()
        new_content = generator.generate_consolidated(companies, reports)

        # Append to file
        with open(file_path, 'a') as f:
            f.write(
                "\n\n* Consolidated Tax Reports - Ticket 231589\n"
                f"* Generated: {datetime.now().isoformat()}\n\n"
            )
            f.write(new_content)

        return True

    def custom_consolidation(self):
        """Custom consolidation setup"""
        print_header("Custom Tax Report Consolidation")
        print("Coming soon...")

    def validate_file(self):
        """Validate PCX export file"""
        print_header("Validate Export File")
        input("Enter file path: ").strip()
        print("Validation coming soon...")
