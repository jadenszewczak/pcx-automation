#!/usr/bin/env python3
"""
PCX Automation CLI
Main entry point for PCX import/export automation tools
"""

import argparse
import sys
from modules import commitment_books
from utils.formatters import print_header, print_error


class PCXAutomationCLI:
    def __init__(self):
        # Only include modules that exist
        self.modules = {
            '1': {
                'name': 'Commitment Book Management',
                'handler': commitment_books.CommitmentBookModule()
            },
            # These will be uncommented as we create them:
            # '2': {
            #     'name': 'User Management',
            #     'handler': user_management.UserManagementModule()
            # },
            # '3': {
            #     'name': 'Report Breakouts',
            #     'handler': report_breakouts.ReportBreakoutModule()
            # },
            # '4': {
            #     'name': 'Destination Management',
            #     'handler': destinations.DestinationModule()
            # }
        }

    def display_menu(self):
        """Display main menu"""
        print_header("PCX Automation Tool")
        print("\nMain Menu:")
        print("-" * 40)

        for key, module in self.modules.items():
            print(f"{key}. {module['name']}")

        print("5. Bulk Operations")
        print("6. Export Configuration")
        print("7. Import Configuration")
        print("0. Exit")
        print("-" * 40)

    def run(self):
        """Main CLI loop"""
        while True:
            self.display_menu()
            choice = input("\nSelect an option: ").strip()

            if choice == '0':
                print("\nExiting PCX Automation Tool...")
                sys.exit(0)
            elif choice in self.modules:
                self.modules[choice]['handler'].run()
            elif choice == '5':
                self.bulk_operations()
            elif choice == '6':
                self.export_config()
            elif choice == '7':
                self.import_config()
            else:
                print_error("Invalid option. Please try again.")

            input("\nPress Enter to continue...")

    def bulk_operations(self):
        """Handle bulk operations from CSV/Excel"""
        print_header("Bulk Operations")
        print("1. Import from CSV")
        print("2. Import from Excel")
        print("3. Back to main menu")
        # TODO: Implementation

    def export_config(self):
        """Export current configuration"""
        print_header("Export Configuration")
        # TODO: Implementation
        print("This feature is coming soon...")

    def import_config(self):
        """Import configuration"""
        print_header("Import Configuration")
        # TODO: Implementation
        print("This feature is coming soon...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PCX Automation CLI Tool')
    parser.add_argument('--module', '-m', help='Jump directly to a module')
    parser.add_argument(
        '--batch', '-b',
        help='Run in batch mode with config file'
    )

    args = parser.parse_args()

    cli = PCXAutomationCLI()

    if args.batch:
        # TODO: Handle batch mode
        print("Batch mode not yet implemented")
    else:
        cli.run()
