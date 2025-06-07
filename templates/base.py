"""Base template class for PCX template generation"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseTemplate(ABC):
    """Base class for all PCX template generators"""

    def __init__(self):
        """Initialize base template"""
        self.field_width = 30  # Standard PCX field width for alignment

    def format_field(self, key: str, value: str) -> str:
        """Format a key-value pair with proper PCX spacing"""
        # PCX format requires keys padded to column 30
        return f"    {key:<{self.field_width - 4}} = {value}"

    def generate_block(self, block_type: str, fields: Dict[str, Any]) -> str:
        """Generate a formatted PCX block"""
        lines = [f"ADD {block_type}"]

        for key, value in fields.items():
            # Skip None values
            if value is not None:
                lines.append(self.format_field(key, str(value)))

        return "\n".join(lines)

    @abstractmethod
    def generate(self, **kwargs) -> str:
        """Generate template output - must be implemented by subclasses"""
        pass
