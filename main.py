import sys
import re
import pandas as pd

SHEET_PATH = "./data.xls"
OUT_PATH   = "./data.csv"

WALL_TYPE_MAP = {
  "MASS"         : "BTAP-ExteriorWall-Mass-",
  "METAL"        : "BTAP-ExteriorWall-Metal-",
  "STEEL FRAMED" : "BTAP-ExteriorWall-SteelFramed-",
  "WOOD FRAMED"  : "BTAP-ExteriorWall-WoodFramed-",
  "IEAD4"        : "BTAP-ExteriorRoof-Mass-" # this is a roof
}

# TODO: "jamb" is missing, also verify the non-convex values 
CONSTRUCTION_TYPE_MAP = {
  "BTAP-IntermediateFloorEdge" : "transition",
  "BTAP-GlazingPerimeter"      : "sill",
  "BTAP-Parapet"               : "parapetconvex",
  "BTAP-RoofCurbs"             : "head",
  "BTAP-Grade"                 : "gradeconvex",
  "BTAP-Corner"                : "cornerconvex"
}

class Sheet:
  def __init__(self, sheet_name, save_name):
    self.sheet_name = sheet_name
    self.save_name  = save_name

SHEETS = [
  Sheet("Thermal Bridging", "thermal_bridging_data.json")
]
SHEET_NAMES = list(map(lambda x: x.sheet_name, SHEETS))

def main() -> None:
  if len(sys.argv) < 2 or sys.argv[1] not in SHEET_NAMES:
    print(f"Usage: python3 ./main.py ({'|'.join(SHEET_NAMES)})")

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


  dfs = []
  df = pd.read_excel(SHEET_PATH, sheet_name = sheet.sheet_name, skiprows = 1)
  df.columns = columns
  df = df.ffill()

  # Reformat column B to match the way the materials are spelled in BTAP
  # Example: 
  # BTAP-EXTERIOR WALL STEEL FRAMED- 2 
  # becomes
  # BTAP-ExteriorWall-SteelFramed-2 good

  for _, entry in df.iterrows():
    wall_reference    = entry["Wall Reference"]
    construction_name = entry["construction_type_name"]
    construction_type = CONSTRUCTION_TYPE_MAP[construction_name[:construction_name.rindex("-")]]
    formatted_entries = []

    match = match_wall_type(wall_reference)

    # Some entries have two references
    if len(re.findall(r"BTAP", wall_reference)) == 2:

      # All compound entries have SteelFramed as the first
      try:
        wall_reference_1, wall_reference_2 = wall_reference.split("& BTAP")
      except ValueError as e:
        print(e)
        import IPython; IPython.embed(); exit()

      match_2 = match_wall_type(wall_reference_2)
      formatted_entries = \
        format_subtypes(wall_reference_1, entry["Quality of Detail"], match) + \
        format_subtypes(wall_reference_2, entry["Quality of Detail"], match_2)

    else:
      formatted_entries = format_subtypes(wall_reference, entry["Quality of Detail"], match) 
            
    if not formatted_entries:
      print("Empty formatted entries")
      import IPython; IPython.embed(); exit()
      raise Exception(f"Error: Could not generate any entries for series\n{entry}")

    num_formatted = len(formatted_entries)
    dfs.append(pd.DataFrame(data = {
      "construction_name" : [construction_name]      * num_formatted,
      "construction_type" : [construction_type]      * num_formatted,
      "wall_reference"    : formatted_entries,
      "description_x"     : [entry["description_x"]] * num_formatted,
      "description_y"     : [entry["description_y"]] * num_formatted,
      "u_w_per_m_k"       : [entry["u_w_per_m_k"]]   * num_formatted,
      "id_layers"         : [entry["Material ID"]]   * num_formatted,
      "multipliers"       : [entry["Multiplier"]]    * num_formatted 
    }))

  df = pd.concat(dfs)

  # ID Layers and multipliers need to be in the same row, find duplicates and
  # merge them
  df = df.groupby(
    ["construction_name", "construction_type", "wall_reference", "description_x", "description_y", "u_w_per_m_k"],
    as_index=False,
    sort=False
  ).agg({
    "id_layers": lambda x: ",".join(map(str, x)),
    "multipliers": lambda x: ",".join(map(str, x))
  })

  df.to_csv(OUT_PATH, index = False)
  
def match_wall_type(name):
  # Match a type to a wall name and catch errors

  match_return = None
  for match in WALL_TYPE_MAP.keys():
    if match in name:
      match_return = match

  if not match_return:
    raise Exception(f"Error: Could not find match for construction ({name})")

  return match_return
  
def format_subtypes(name: str, quality: str, match: str):
  # Separate rows with constructions containing multiple suffixes into their own rows

  # Retrieve alphanumeric suffixes associated with the construction types
  subtypes = re.findall(r"\d{1,2}[BC]?", name)

  # TODO: Verify if this is true
  # SteelFramed-1 is not present in the spreadsheet but it should be equal to SteelFramed-2
  if "2" in subtypes:
    subtypes.append("1")

  # TODO: Verify if this is correct
  # Spreadsheet has "Fair" and "Best" qualtiy specifiers but it seems only
  # "good" and "bad" exist in BTAP
  if quality == "Fair" or quality == "Best":
    quality = "good"

  return [f"{WALL_TYPE_MAP[match]}{subtype} {quality.lower()}" for subtype in subtypes]
  
  
if __name__ == "__main__":
  main()
