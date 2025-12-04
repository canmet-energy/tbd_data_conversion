SHEET_DATA_PATH       = "./data.xls"
UFACTORS_CORRECT_PATH = "./ufactors_converted.json"
THERMAL_BRIDGING_PATH = "./thermal_bridging_data.csv"
OPAQUE_PATH           = "./materials_opaque.csv"
GLAZING_PATH          = "./materials_glazing.csv"
CONSTRUCTION_PAIRS    = [
  ("DOORS",          "./constructions_door.json"),
  ("EXPFLOOR",       "./constructions_floor.json"),
  ("WALLS",          "./constructions_wall.json"),
  ("BG-WALL",        "./constructions_bg_wall.json"),
  ("ROOF",           "./constructions_roof.json"),
  ("BG-ROOF",        "./constructions_bg_roof.json"),
  ("SLAB",           "./constructions_slab.json"),
  ("ExteriorWindow", "./constructions_window.json"),
  ("GlassDoor",      "./constructions_door_glass.json"),
  ("Skylight",       "./constructions_skylight.json")
]
CONSTRUCTION_QAQC     = "./constructions_qaqc.txt"

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

CONSTRUCTION_ID_MAP = {
  "DOORS"          : "material_opaque_id_layers",
  "EXPFLOOR"       : "material_opaque_id_layers",
  "WALLS"          : "material_opaque_id_layers",
  "BG-WALL"        : "material_opaque_id_layers",
  "ROOF"           : "material_opaque_id_layers",
  "BG-ROOF"        : "material_opaque_id_layers",
  "SLAB"           : "material_opaque_id_layers",
  "ExteriorWindow" : "material_glazing_id_layers",
  "GlassDoor"      : "material_glazing_id_layers",
  "Skylight"       : "material_glazing_id_layers"
}
