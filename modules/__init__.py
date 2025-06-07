"""Base module class for PCX operations"""

from abc import ABC, abstractmethod
from utils.formatters import print_error


class BaseModule(ABC):
    """Base class for all PCX automation modules"""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def display_menu(self):
        """Display module-specific menu"""
        pass

    @abstractmethod
    def run(self):
        """Run the module"""
        pass

    def get_input(
        self, prompt: str, required: bool = True, validator=None
    ) -> str:
        """Get user input with optional validation"""
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
