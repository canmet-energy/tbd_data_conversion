import pandas as pd
import common

# Convert new materials_opaque and materials_glazing entries
# Only convert the section that contains the new entries 
# (entries after 157 for opaque and 35 for glazing)
# TODO: These values are only from Vancouver--how should we cost these for other cities?
def convert_materials() -> None:
  empty_opaque_columns = [
    "material_op_factor",
    "labour_op_factor",
    "equipment_op_factor",
    "comments",
    "quantity",
    "material_mult",
    "labour_mult",
    "op_mult",
    "eqpt"
  ]

  empty_glazing_columns = [
    "catalog_id",
    "equipment_cost",
    "material_op_factor",
    "labour_op_factor",
    "equipment_op_factor",
    "fenestration_frame_type",
    "fenestration_divider_type",
    "fenestration_tint",
    "fenestration_gas_fill",
    "fenestration_low_emissivity_coating",
    "solar_heat_gain_coefficient",
    "visible_transmittance",
    "comments"
  ]

  df_opaque  = pd.read_excel(common.SHEET_DATA_PATH, sheet_name = "OpaqueMaterials", skiprows = range(1, 157))
  df_glazing = pd.read_excel(common.SHEET_DATA_PATH, sheet_name = "GlazingMaterials", skiprows = range(1, 35))
  df_opaque.drop([df_opaque.columns[0]] + empty_opaque_columns, axis = 1, inplace = True)
  df_glazing.drop([df_glazing.columns[0]] + empty_glazing_columns, axis = 1, inplace = True)
  df_opaque.to_csv(common.OPAQUE_PATH, index = False)
  df_glazing.to_csv(common.GLAZING_PATH, index = False)

convert_materials()
