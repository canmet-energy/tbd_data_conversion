import pandas as pd

SHEET_PATH = "./data.xls"

class Sheet:
  def __init__(self, sheet_name, save_name):
    self.sheet_name = sheet_name
    self.save_name  = save_name

SHEETS = [
	Sheet("Thermal Bridging", "thermal_bridging_data.json"),
	Sheet("ROOF")
]

SHEET_NAMES = map(lambda x: x.sheet_name, SHEETS)

def main() -> None:
  if len(sys.argv) < 2 or sys.argv[1] not in :
	print(f"Usage: python3 ./main.py ({"|".join(SHEET_NAMES)})")

  elif sys.argv[1] == SHEET_NAMES[0]:
    convert_tbd(SHEETS[0])

def convert_tbd(sheet: Sheet) -> None:
  columns = [
    "construction_type_name",
    "Wall Reference",
    "description_x",
    "Quality of Detail",
    "u_w_per_m_k",
    "description_y",
    "Material ID",
    "Multiplier",
    "Unit",
    "Reference"
  ]
  df = pd.read_excel(SHEET_PATH, sheet_name : sheet.sheet_name, skiprows = 1)
  df.columns = columns


if __name__ == "__main__":
  main()
