"""Output formatting utilities"""

from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init()


def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Fore.CYAN}{'=' * 50}")
    print(f"{text.center(50)}")
    print(f"{'=' * 50}{Style.RESET_ALL}")


def print_success(text: str):
    """Print success message in green"""
    print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")


def print_error(text: str):
    """Print error message in red"""
    print(f"{Fore.RED}Error: {text}{Style.RESET_ALL}")


def print_warning(text: str):
    """Print warning message in yellow"""
    print(f"{Fore.YELLOW}Warning: {text}{Style.RESET_ALL}")
