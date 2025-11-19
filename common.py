class Sheet:
  def __init__(self, sheet_name, save_name):
    self.sheet_name = sheet_name
    self.save_name  = save_name

SHEETS = [
  Sheet("Thermal Bridging", "thermal_bridging_data.csv"),
  Sheet("OpaqueMaterials", "materials_opaque.csv")
]

SHEET_NAMES = list(map(lambda x: x.sheet_name, SHEETS))

SHEET_PATH = "./data.xls"
UFACTORS_CORRECT = "./ufactors_converted.json"
THERMAL_BRIDGING_DATA = "./thermal_bridging_data.csv"

# U-Factors defined by Denis to be validated against the excel data
CORRECT_U_FACTORS = "./ufactors-converted.py"

WALL_TYPE_MAP = {
  "MASS"         : "BTAP-ExteriorWall-Mass-",
  "METAL"        : "BTAP-ExteriorWall-Metal-",
  "STEEL FRAMED" : "BTAP-ExteriorWall-SteelFramed-",
  "WOOD FRAMED"  : "BTAP-ExteriorWall-WoodFramed-",
  "IEAD4"        : "BTAP-ExteriorRoof-Mass-" # this is a roof
}

CONSTRUCTION_TYPE_MAP = {
  "BTAP-IntermediateFloorEdge" : "rimjoist",     # rim joist
  "BTAP-GlazingPerimeter"      : "fenestration", # jamb (side), sill (bottom), head (top) (fenestration)
  "BTAP-Parapet"               : "parapet",  
  "BTAP-RoofCurbs"             : "", # Roof curbs currently aren't relevant.
  "BTAP-Grade"                 : "grade",
  "BTAP-Corner"                : "corner"
}

