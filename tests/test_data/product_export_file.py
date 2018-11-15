"""Response data for the ViewFile request."""

from pathlib import Path

path = Path(__file__).parent / "product_export_file.xlsx"

with open(str(path), "rb") as f:
    PRODUCT_EXPORT_FILE = f.read()
