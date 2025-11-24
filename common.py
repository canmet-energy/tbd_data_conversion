SHEET_DATA_PATH       = "./data.xls"
UFACTORS_CORRECT_PATH = "./ufactors_converted.json"
THERMAL_BRIDGING_PATH = "./thermal_bridging_data.csv"
OPAQUE_PATH           = "./materials_opaque.csv"
GLAZING_PATH          = "./materials_glazing.csv"

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

