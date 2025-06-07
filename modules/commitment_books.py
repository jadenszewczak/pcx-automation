"""Commitment Book Management Module"""

from datetime import datetime
from typing import Dict, List
from modules import BaseModule
from config.mappings import COMMITMENT_BOOKS
from config.settings import GENERATED_DIR
from templates.destination import DestinationTemplate
from templates.rule import RuleTemplate
from utils.validators import validate_store_number
from utils.formatters import print_header, print_success, print_error


class CommitmentBookModule(BaseModule):
    def __init__(self):
        super().__init__("Commitment Book Management")
        self.destination_template = DestinationTemplate()
        self.rule_template = RuleTemplate()

    def display_menu(self):
        """Display commitment book menu"""
        print_header(self.name)
        print("\n1. Add single store")
        print("2. Add multiple stores")
        print("3. Generate from CSV")
        print("4. View commitment book types")
        print("5. Back to main menu")

    def run(self):
        """Run commitment book module"""
        while True:
            self.display_menu()
            choice = input("\nSelect an option: ").strip()

            if choice == '1':
                self.add_single_store()
            elif choice == '2':
                self.add_multiple_stores()
            elif choice == '3':
                self.generate_from_csv()
            elif choice == '4':
                self.view_commitment_types()
            elif choice == '5':
                break
            else:
                print_error("Invalid option.")

    def add_single_store(self):
        """Add commitment books for a single store"""
        print_header("Add Single Store")

        # Collect store information
        store_info = self.collect_store_info()

        # Show summary
        self.display_summary([store_info])

        if self.confirm_action("Generate commitment books for this store?"):
            self.generate_files([store_info])

    def add_multiple_stores(self):
        """Add commitment books for multiple stores"""
        print_header("Add Multiple Stores")

        stores = []
        while True:
            print(f"\nStore #{len(stores) + 1}")
            store_info = self.collect_store_info()
            stores.append(store_info)

            if not self.confirm_action("Add another store?"):
                break

        self.display_summary(stores)

        if self.confirm_action("Generate commitment books for all stores?"):
            self.generate_files(stores)

    def collect_store_info(self) -> Dict[str, str]:
        """Collect store information from user"""
        store_info = {}

        # Store number with validation
        store_info['number'] = self.get_input(
            "Store number: ",
            validator=validate_store_number
        )

        # Store name
        store_info['name'] = self.get_input("Store name: ")

        # Address
        store_info['address'] = self.get_input("Street address: ")

        # City, State, Zip
        store_info['city_state_zip'] = self.get_input("City, State ZIP: ")

        # Optional: Select specific commitment books
        if self.confirm_action(
            "Select specific commitment books? (default: all)"
        ):
            store_info['books'] = self.select_commitment_books()
        else:
            store_info['books'] = list(COMMITMENT_BOOKS.keys())

        return store_info

    def select_commitment_books(self) -> List[str]:
        """Allow user to select specific commitment books"""
        selected = []

        print("\nAvailable commitment books:")
        for i, book in enumerate(COMMITMENT_BOOKS.keys(), 1):
            print(f"{i}. {book}")

        prompt = "\nEnter numbers separated by commas (or 'all'): "
        selections = input(prompt).strip()

        if selections.lower() == 'all':
            return list(COMMITMENT_BOOKS.keys())

        try:
            indices = [int(x.strip()) - 1 for x in selections.split(',')]
            books = list(COMMITMENT_BOOKS.keys())
            selected = [books[i] for i in indices if 0 <= i < len(books)]
        except (ValueError, IndexError):
            print_error("Invalid selection. Using all books.")
            return list(COMMITMENT_BOOKS.keys())

        return selected

    def generate_files(self, stores: List[Dict[str, str]]):
        """Generate destination and rule files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        destinations_file = GENERATED_DIR / f"destinations_{timestamp}.txt"
        rules_file = GENERATED_DIR / f"rules_{timestamp}.txt"

        destinations_content = "* Defined Destinations\n\n"
        rules_content = "* Defined Rules\n\n"

        for store in stores:
            # Generate destinations
            dest_result = self.generate_destinations(store)
            destinations_content += dest_result

            # Generate rules
            rules_result = self.generate_rules(store)
            rules_content += rules_result

        # Write files
        with open(destinations_file, 'w') as f:
            f.write(destinations_content)

        with open(rules_file, 'w') as f:
            f.write(rules_content)

        print_success("\nFiles generated successfully:")
        print(f"  Destinations: {destinations_file}")
        print(f"  Rules: {rules_file}")

        # Optionally combine into single import file
        if self.confirm_action("\nCombine into single import file?"):
            combined_file = GENERATED_DIR / f"pcx_import_{timestamp}.txt"
            with open(combined_file, 'w') as f:
                f.write(destinations_content)
                f.write("\n\n")
                f.write(rules_content)
            print_success(f"  Combined: {combined_file}")

    def generate_destinations(self, store: Dict[str, str]) -> str:
        """Generate destination blocks for a store"""
        content = ""

        # Generate printer destinations
        queues = set(
            book['queue']
            for book in COMMITMENT_BOOKS.values()
            if book['queue']
        )
        for queue in queues:
            dest = self.destination_template.generate_printer(
                queue=queue,
                store_number=store['number'],
                store_name=store['name'],
                address=store['address'],
                city_state_zip=store['city_state_zip']
            )
            content += dest + "\n\n"

        # Generate folder destinations
        for book_name in store['books']:
            dest = self.destination_template.generate_folder(
                report="RABOC010",
                job=book_name,
                identifier=store['number']
            )
            content += dest + "\n\n"

        return content

    def generate_rules(self, store: Dict[str, str]) -> str:
        """Generate rule blocks for a store"""
        content = ""

        for book_name in store['books']:
            book_config = COMMITMENT_BOOKS[book_name]
            rule = self.rule_template.generate_commitment_rule(
                report="RABOC010",
                job=book_name,
                store_number=store['number'],
                variable=book_config['variable'],
                queue=book_config['queue']
            )
            content += rule + "\n\n"

        return content

    def display_summary(self, stores: List[Dict[str, str]]):
        """Display summary of stores to be processed"""
        print_header("Summary")
        print(f"\nTotal stores: {len(stores)}")

        for i, store in enumerate(stores, 1):
            print(f"\nStore {i}:")
            print(f"  Number: {store['number']}")
            print(f"  Name: {store['name']}")
            print(f"  Books: {len(store['books'])}")

    def view_commitment_types(self):
        """Display available commitment book types"""
        print_header("Commitment Book Types")

        print("\nBook Name    | Variable            | Queue")
        print("-" * 50)

        for book, config in COMMITMENT_BOOKS.items():
            print(f"{book:<12} | {config['variable']:<18} | {config['queue']}")

        input("\nPress Enter to continue...")
