"""Commitment Book module for PCX operations"""

from abc import ABC, abstractmethod
from typing import Callable, Optional
from utils.formatters import print_error, print_header, print_success


class BaseModule(ABC):
    """Base class for all PCX automation modules"""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def display_menu(self) -> None:
        """Display module-specific menu"""
        pass

    @abstractmethod
    def run(self) -> None:
        """Run the module"""
        pass

    def get_input(
        self,
        prompt: str,
        required: bool = True,
        validator: Optional[Callable[[str], bool]] = None
    ) -> str:
        """Get user input with optional validation

        Args:
            prompt: The prompt to display to the user
            required: Whether the input is required
            validator: Optional function that takes a string and returns bool

        Returns:
            The validated user input string
        """
        while True:
            value = input(prompt).strip()

            if not value and not required:
                return value

            if not value and required:
                print_error("This field is required.")
                continue

            if validator and not validator(value):
                continue

            return value

    def confirm_action(self, message: str) -> bool:
        """Confirm user action"""
        response = input(f"\n{message} (y/n): ").strip().lower()
        return response == 'y'


class CommitmentBookModule(BaseModule):
    """Commitment Book Management module"""

    def __init__(self) -> None:
        super().__init__("Commitment Book Management")

    def display_menu(self) -> None:
        print_header(self.name)
        print("\n1. View Commitment Books")
        print("2. Add Commitment Book")
        print("3. Remove Commitment Book")
        print("4. Back to main menu")

    def run(self) -> None:
        while True:
            self.display_menu()
            choice = input("\nSelect an option: ").strip()
            if choice == '1':
                print_success("Viewing commitment books (not implemented).")
            elif choice == '2':
                print_success("Adding commitment book (not implemented).")
            elif choice == '3':
                print_success("Removing commitment book (not implemented).")
            elif choice == '4':
                break
            else:
                print_error("Invalid option.")

    def process_ticket_231589_quick(self) -> None:
        print_header("Quick process for ticket #231589 (not implemented).")
