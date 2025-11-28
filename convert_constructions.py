import pandas as pd
import json
import common

FIBREGLASS_WINDOW_PSI_MAP = {
  1.44 : (45, "Cascadia Universal Series, double glazed, 2x low-e coatings, Stainless Steel Spacer, U=1.13W/m2K"),
  1.4  : (45, "Cascadia Universal Series, double glazed, 2x low-e coatings, Stainless Steel Spacer, U=1.13W/m2K"),
  0.8  : (46, "Cascadia Universal Series, triple glazed, 3x low-e coatings, tri-seal spacer, U=0.77W/m2K")
}

FIBRELGASS_DOOR_MAP = {
  1.44 : (53, "Cascadia Universal Series, double glazed, 2x low-e coatings, Stainless Steel Spacer, U=1.13W/m2K"),
  1.4  : (53, "Cascadia Universal Series, double glazed, 2x low-e coatings, Stainless Steel Spacer, U=1.13W/m2K"),
  0.8  : (54, "Cascadia Universal Series, triple glazed, 3x low-e coatings, tri-seal spacer, U=0.77W/m2K")
}

def convert_constructions() -> None:
  with open(common.CONSTRUCTION_QAQC, "w") as qaqc_file:
    for sheet_name, file_name in common.CONSTRUCTION_PAIRS:
      df = pd.read_excel(common.SHEET_DATA_PATH, sheet_name = sheet_name)
      id_column = common.CONSTRUCTION_ID_MAP[sheet_name]
      
      df["construction_type_name"] = df["construction_type_name"].ffill()
      df["description_x"]          = df["description_x"].ffill()
      df["u_w_per_m2_k"]           = df["u_w_per_m2_k"].ffill()
      df["u_w_per_m2_k"]           = df["u_w_per_m2_k"].round(3)
      
      # All empty ID entries except from BG-ROOF are from windows which refer 
      # to the fiberglass window. Assuming the PSI values of these empty layers
      # should map directly to the fibreglass window.
      df_empty_ids = df[df[id_column].isnull()]
      psi_map = None
      if not df_empty_ids.empty:
        print(f"Empty ID indices for {sheet_name}: {list(df_empty_ids.index)}\n", file = qaqc_file)
        if sheet_name == "ExteriorWindow":
          psi_map = FIBREGLASS_WINDOW_PSI_MAP
        elif sheet_name == "GlassDoor":
          psi_map = FIBRELGASS_DOOR_MAP
        elif sheet_name == "BG-ROOF":
          df.drop(df_empty_ids.index, inplace = True)
        else:
          # import IPython; IPython.embed(); exit()
          raise Exception("You should not be here exception")

        if psi_map:
          for psi, (material_id, description) in psi_map.items():
            mask = df_empty_ids["u_w_per_m2_k"] == psi
            df.loc[df_empty_ids[mask].index, id_column] = material_id
            df.loc[df_empty_ids[mask].index, "description_y"] = description
      
      df = df.set_index(["construction_type_name", "u_w_per_m2_k"])
      json_data = {}
      for (construction, psi), group in df.groupby(level = [0, 1]):
        if construction not in json_data:
          json_data[construction] = {"psi" : {}}
        json_data[construction]["psi"][psi] = {
          "description": group.iloc[0]["description_x"],
          id_column: [
            {"id": int(row[id_column]), "description": row["description_y"]}
            for _, row in group.iterrows()
          ]
        }
      
      with open(file_name, "w") as file:
        json.dump(json_data, file, indent = 4)

convert_constructions()

