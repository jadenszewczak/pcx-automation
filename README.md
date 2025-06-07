# PCX Automation Tool

Internal CLI tool for automating PCX/VPSX administrative tasks.

## Features

- ✅ Commitment Book Management
  - Single/multiple store setup
  - Bulk generation from templates
  - All 9 commitment book types
  
- 🚧 User Management (Coming Soon)
- 🚧 Report Breakouts (Coming Soon)  
- 🚧 Destination Management (Coming Soon)

## Setup

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the CLI tool:
```bash
python pcx_cli.py
```

## Project Structure

```
pcx-automation/
├── pcx_cli.py           # Main CLI entry point
├── config/              # Configuration and mappings
├── modules/             # Feature modules
├── templates/           # PCX template generators
├── utils/               # Utilities and helpers
└── data/                # Generated files
```

## Development

- Python 3.11+
- Virtual environment recommended
- Follow existing patterns when adding new modules
