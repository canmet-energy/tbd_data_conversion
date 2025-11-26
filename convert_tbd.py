import re
import pandas as pd
import common

def convert_tbd():
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
  df = pd.read_excel(common.SHEET_DATA_PATH, sheet_name = "Thermal Bridging", skiprows = 1)
  df.columns = columns
  df.ffill(inplace = True)

  # Reformat column B to match the way the materials are spelled in BTAP
  # Example: 
  # BTAP-EXTERIOR WALL STEEL FRAMED- 2 
  # becomes
  # BTAP-ExteriorWall-SteelFramed-2 good

  for _, entry in df.iterrows():
    wall_reference    = entry["Wall Reference"]
    construction_name = entry["construction_type_name"]
    construction_type = common.CONSTRUCTION_TYPE_MAP[construction_name[:construction_name.rindex("-")]]

    # Skip undefined constructions (for now only RoofCurbs)
    if not construction_type:
      continue

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
      "construction_name"              : [construction_name]      * num_formatted,
      "edge_type"                      : [construction_type]      * num_formatted,
      "wall_reference"                 : formatted_entries,
      "description_x"                  : [entry["description_x"]] * num_formatted,
      "description_y"                  : [entry["description_y"]] * num_formatted,
      "u_w_per_m_k"                    : [entry["u_w_per_m_k"]]   * num_formatted,
      "material_opaque_id_layers"      : [entry["Material ID"]]   * num_formatted,
      "id_layers_quantity_multipliers" : [entry["Multiplier"]]    * num_formatted, 
      "unit"                           : [entry["Unit"]]          * num_formatted, 
    }))

  df = pd.concat(dfs)

  # ID Layers and multipliers need to be in the same row, find duplicates and
  # merge them
  df = df.groupby(
    ["construction_name", "edge_type", "wall_reference", "description_x", "description_y", "u_w_per_m_k"],
    as_index=False,
    sort=False
  ).agg({
    "material_opaque_id_layers" : lambda x: ",".join(map(str, x)),
    "id_layers_quantity_multipliers" : lambda x: ",".join(map(str, x))
  })

  df.to_csv(common.THERMAL_BRIDGING_PATH, index = False)

def match_wall_type(name):
  # Match a type to a wall name and catch errors

  match_return = None
  for match in common.WALL_TYPE_MAP.keys():
    if match in name:
      match_return = match

  if not match_return:
    raise Exception(f"Error: Could not find match for construction ({name})")

  return match_return
  
def format_subtypes(name: str, quality: str, match: str):
  # Separate rows with constructions containing multiple suffixes into their own rows

  # Retrieve alphanumeric suffixes associated with the construction types
  subtypes = re.findall(r"\d{1,2}[BC]?", name)

  # SteelFramed-1 is not present in the spreadsheet but it should be equal to SteelFramed-2
  if "2" in subtypes:
    subtypes.append("1")

  # Spreadsheet has "Fair" and "Best" qualtiy specifiers but it seems only
  # "good" and "bad" exist in BTAP
  # Denis: Fair should map to good, entries with "Best" can be ignored
  if quality == "Fair" or quality == "Best":
    quality = "good"

  return [f"{common.WALL_TYPE_MAP[match]}{subtype} {quality.lower()}" for subtype in subtypes]

convert_tbd()
