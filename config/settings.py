"""Global settings for PCX Automation"""

from pathlib import Path
from typing import TypedDict

# Base paths
BASE_DIR: Path = Path(__file__).parent.parent
DATA_DIR: Path = BASE_DIR / 'data'
EXPORT_DIR: Path = DATA_DIR / 'exports'
GENERATED_DIR: Path = DATA_DIR / 'generated'

# Ensure directories exist
for dir_path in [DATA_DIR, EXPORT_DIR, GENERATED_DIR]:
    dir_path.mkdir(exist_ok=True, parents=True)


# Define typed configuration structures
class PCXConfigType(TypedDict):
    """Type definition for PCX configuration"""
    print_server: str
    default_copies: int
    date_format: str


class FileNamingType(TypedDict):
    """Type definition for file naming conventions"""
    destinations: str
    rules: str
    combined: str


# PCX Configuration with strong typing
PCX_CONFIG: PCXConfigType = {
    'print_server': 'vpsx',
    'default_copies': 2,
    'date_format': '%Y%m%d_%H%M%S'
}

# File naming conventions with strong typing
FILE_NAMING: FileNamingType = {
    'destinations': 'destinations_{timestamp}.txt',
    'rules': 'rules_{timestamp}.txt',
    'combined': 'pcx_import_{timestamp}.txt'
}
