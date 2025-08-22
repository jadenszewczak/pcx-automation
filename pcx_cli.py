#!/usr/bin/env python3
"""
PCX Automation CLI
Main entry point for PCX import/export automation tools
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Protocol
from utils.formatters import (
    print_header, print_error, print_warning, print_success
)


class ModuleHandler(Protocol):
    """Protocol defining the interface for module handlers"""
    def run(self) -> None: ...
    def process_ticket_231589_quick(self) -> None: ...


# Type alias for module dictionary
ModuleInfo = Dict[str, Any]


class PCXAutomationCLI:
    def __init__(self) -> None:
        # Build modules dictionary with proper typing
        self.modules: Dict[str, ModuleInfo] = {}

        # Try to import commitment books module
        try:
            from modules.commitment_books import CommitmentBookModule
            self.modules['1'] = {
                'name': 'Commitment Book Management',
                'handler': CommitmentBookModule()
            }
        except ImportError as e:
            print_warning(f"Commitment Book module not available: {e}")

        # Try to import tax module if available
        try:
            from modules.tax_reports import TaxReportModule
            self.modules['2'] = {
                'name': '🚨 Tax Report Consolidation (EMERGENCY)',
                'handler': TaxReportModule()
            }
        except ImportError:
            # Tax module is optional
            pass

    def display_menu(self) -> None:
        """Display main menu"""
        print_header("PCX Automation Tool")

        # Check for emergency tickets
        if '2' in self.modules:
            print_warning("⚠️  EMERGENCY TICKET #231589 ACTIVE - Use Option 2")

        print("\nMain Menu:")
        print("-" * 40)

        for key, module in self.modules.items():
            module_name: str = module['name']
            # Highlight emergency module
            if 'EMERGENCY' in module_name:
                print(f">>> {key}. {module_name} <<<")
            else:
                print(f"{key}. {module_name}")

        if not self.modules:
            print("No modules available. Check installation.")

        print("\n--- Utilities ---")
        print("5. Bulk Operations")
        print("6. Export Configuration")
        print("7. Import Configuration")
        print("8. Validate PCX File")
        print("0. Exit")
        print("-" * 40)

    def run(self, quick_action: Optional[str] = None) -> None:
        """Main CLI loop

        Args:
            quick_action: Optional action to run immediately
        """
        # Handle quick actions for emergency tickets
        if quick_action == 'ticket-231589':
            if '2' in self.modules:
                print_header("EMERGENCY: Processing Ticket #231589")
                handler = self.modules['2']['handler']
                # Check if the handler has the quick method
                if hasattr(handler, 'process_ticket_231589_quick'):
                    handler.process_ticket_231589_quick()
                return
            else:
                print_error(
                    "Tax module not available! "
                    "Create modules/tax_reports.py"
                )
                return

        while True:
            self.display_menu()
            choice = input("\nSelect an option: ").strip()

            if choice == '0':
                print("\nExiting PCX Automation Tool...")
                sys.exit(0)
            elif choice in self.modules:
                handler = self.modules[choice]['handler']
                handler.run()
            elif choice == '5':
                self.bulk_operations()
            elif choice == '6':
                self.export_config()
            elif choice == '7':
                self.import_config()
            elif choice == '8':
                self.validate_pcx_file()
            else:
                print_error("Invalid option. Please try again.")

            if choice not in ['0']:  # Don't pause on exit
                input("\nPress Enter to continue...")

    def bulk_operations(self) -> None:
        """Handle bulk operations from CSV/Excel"""
        print_header("Bulk Operations")
        print("\n1. Import from CSV")
        print("2. Import from Excel")
        print("3. Process multiple tickets")
        print("4. Back to main menu")

        choice = input("\nSelect option: ").strip()

        if choice == '1':
            print_warning("CSV import coming soon...")
        elif choice == '2':
            print_warning("Excel import coming soon...")
        elif choice == '3':
            print_warning("Multi-ticket processing coming soon...")
        elif choice == '4':
            return
        else:
            print_error("Invalid option")

    def export_config(self) -> None:
        """Export current configuration"""
        print_header("Export Configuration")
        print("\nThis will export your current PCX configuration.")
        print("Export location: data/exports/")

        export_type = input("\nExport type (full/partial): ").strip().lower()

        if export_type == 'full':
            print_warning("Full export coming soon...")
        elif export_type == 'partial':
            print_warning("Partial export coming soon...")
        else:
            print_error("Invalid export type")

    def import_config(self) -> None:
        """Import configuration"""
        print_header("Import Configuration")
        print("\n⚠️  WARNING: This will modify your PCX configuration!")

        file_path = input("\nEnter import file path: ").strip()

        if not file_path:
            print_error("No file specified")
            return

        if not Path(file_path).exists():
            print_error(f"File not found: {file_path}")
            return

        print_warning("Import functionality coming soon...")
        print(f"Would import from: {file_path}")

    def validate_pcx_file(self) -> None:
        """Validate a PCX export file"""
        print_header("PCX File Validator")

        file_path = input("\nEnter PCX file path to validate: ").strip()

        if not file_path:
            print_error("No file specified")
            return

        if not Path(file_path).exists():
            print_error(f"File not found: {file_path}")
            return

        try:
            from utils.pcx_validator import PCXValidator
            validator = PCXValidator()
            is_valid, errors = validator.validate_file(Path(file_path))

            if is_valid:
                print_success("✅ File is valid!")
            else:
                print_error("❌ Validation errors found:")
                for error in errors[:10]:  # Show first 10 errors
                    print(f"  - {error}")
                if len(errors) > 10:
                    print(
                        f"  ... and {len(errors) - 10} more errors"
                    )
        except ImportError:
            print_warning(
                "Validator not available. "
                "Create utils/pcx_validator.py"
            )


def main() -> None:
    """Main entry point for the PCX Automation CLI"""
    parser = argparse.ArgumentParser(
        description='PCX Automation CLI Tool',
        epilog=(
            'For emergency ticket #231589, use: '
            'python pcx_cli.py --emergency-231589'
        )
    )

    parser.add_argument(
        '--module', '-m',
        help='Jump directly to a module (1=Commitment, 2=Tax)'
    )
    parser.add_argument(
        '--batch', '-b',
        help='Run in batch mode with config file'
    )
    parser.add_argument(
        '--validate',
        help='Validate a PCX export file',
        metavar='FILE'
    )

    # Emergency ticket shortcuts
    parser.add_argument(
        '--emergency-231589',
        action='store_true',
        help='Quick process for emergency ticket #231589'
    )
    parser.add_argument(
        '--ticket',
        help='Process specific ticket number',
        metavar='TICKET_NUM'
    )

    args = parser.parse_args()

    cli = PCXAutomationCLI()

    # Handle command line arguments
    if args.emergency_231589:
        print_warning("🚨 EMERGENCY MODE: Processing Ticket #231589")
        print("This will create consolidated tax reports")
        print("for companies 120-147")

        if '2' in cli.modules:
            response = input("\nType 'CONFIRM' to proceed: ")
            if response == 'CONFIRM':
                cli.run(quick_action='ticket-231589')
            else:
                print("Aborted.")
        else:
            print_error("Tax module not installed!")
            print("\nTo fix this:")
            print("1. Create modules/tax_reports.py with the tax report code")
            print("2. Run this command again")

    elif args.validate:
        # Quick validate mode
        if Path(args.validate).exists():
            cli.validate_pcx_file()
        else:
            print_error(f"File not found: {args.validate}")

    elif args.module:
        # Jump to specific module
        if args.module in cli.modules:
            handler = cli.modules[args.module]['handler']
            handler.run()
        else:
            print_error(f"Module {args.module} not found")

    elif args.batch:
        print_warning("Batch mode not yet implemented")
        print(f"Would process batch file: {args.batch}")

    elif args.ticket:
        # Handle specific ticket
        if args.ticket == '231589' and '2' in cli.modules:
            cli.run(quick_action='ticket-231589')
        else:
            print_warning(f"No handler for ticket {args.ticket}")

    else:
        # Normal interactive mode
        cli.run()


if __name__ == "__main__":
    main()
