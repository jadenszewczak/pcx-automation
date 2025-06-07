"""Data mappings for PCX automation"""

# VPSX Queue mappings
VPSX_QUEUES = {
    "OPW2": "OPW2",
    "DFLTJ": "HELD_KONICA"
}

# Commitment book mappings
COMMITMENT_BOOKS = {
    "PBKOC01R": {"variable": "&RPT_R001C002L004", "queue": "OPW2"},
    "PDEOC91R": {"variable": "&RPT_R005C002L004", "queue": "OPW2"},
    "PDEOC01R": {"variable": "&RPT_R005C002L004", "queue": "OPW2"},
    "PDIOC91R": {"variable": "&RPT_R001C002L004", "queue": "OPW2"},
    "PFROC91R": {"variable": "&RPT_R005C002L004", "queue": "OPW2"},
    "PGMOC91R": {"variable": "&RPT_R005C002L004", "queue": "OPW2"},
    "PGROC01R": {"variable": "&RPT_R005C002L004", "queue": "DFLTJ"},
    "PMTOC91R": {"variable": "&RPT_R001C002L004", "queue": "OPW2"},
    "PPROC91R": {"variable": "&RPT_R005C002L004", "queue": "OPW2"}
}

# Report patterns
REPORT_PATTERNS = {
    'folder_destination': '/Reports/{report}~{identifier}/',
    'printer_destination': '{queue}~{type}{identifier}~{copy}'
}
