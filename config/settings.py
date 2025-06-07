"""Global settings for PCX Automation"""

from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
EXPORT_DIR = DATA_DIR / 'exports'
GENERATED_DIR = DATA_DIR / 'generated'

# Ensure directories exist
for dir_path in [DATA_DIR, EXPORT_DIR, GENERATED_DIR]:
    dir_path.mkdir(exist_ok=True, parents=True)

# PCX Configuration
PCX_CONFIG = {
    'print_server': 'vpsx',
    'default_copies': 2,
    'date_format': '%Y%m%d_%H%M%S'
}

# File naming conventions
FILE_NAMING = {
    'destinations': 'destinations_{timestamp}.txt',
    'rules': 'rules_{timestamp}.txt',
    'combined': 'pcx_import_{timestamp}.txt'
}
