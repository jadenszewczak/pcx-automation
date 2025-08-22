"""Base module class for PCX operations"""

from abc import ABC, abstractmethod
from typing import Callable, Optional
from utils.formatters import print_error


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
        """Confirm user action

        Args:
            message: The confirmation message to display

        Returns:
            True if user confirms, False otherwise
        """
        response = input(f"\n{message} (y/n): ").strip().lower()
        return response == 'y'


# Export the base class
__all__ = ['BaseModule']
