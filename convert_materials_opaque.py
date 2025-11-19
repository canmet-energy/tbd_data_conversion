import re
import pandas as pd
import common

def main() -> None:
  convert_materials_opaque

# Only convert the section that contains the new entries (from entry 156 onwards)
# TODO: These values are only from Vancouver--how should we cost these for other cities?
def convert_materials_opaque(sheet: common.Sheet) -> None:
  columns = [
    "materials_opaque_id",
    "description",
    "source",
    "type",
    "material_type",
    "id",
    "unit",
    "quantity",
    "material_mult",
    "labour_mult",
    "op_mult",
    "eqpt"
  ]

  df = pd.read_excel(common.SHEET_PATH, sheet_name = sheet.sheet_name, skiprows = 1)

if __name__ == "__main__":
  main()
