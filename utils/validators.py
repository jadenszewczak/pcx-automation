"""Input validation utilities"""

from utils.formatters import print_error


def validate_store_number(value: str) -> bool:
    """Validate store number format"""
    if not value.isdigit():
        print_error("Store number must be numeric.")
        return False

    if len(value) > 4:
        print_error("Store number must be 4 digits or less.")
        return False

    return True


def validate_choice(value: str, valid_choices: list) -> bool:
    """Validate menu choice"""
    if value not in valid_choices:
        print_error(f"Please select from: {', '.join(valid_choices)}")
        return False
    return True


def validate_yes_no(value: str) -> bool:
    """Validate yes/no response"""
    if value.lower() not in ['y', 'n', 'yes', 'no']:
        print_error("Please enter 'y' or 'n'.")
        return False
    return True
