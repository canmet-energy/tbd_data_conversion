import csv
import json
import common

tbd_data_path      = common.THERMAL_BRIDGING_PATH # CSV file to validate against
ufactors_data_path = common.UFACTORS_CORRECT_PATH # JSON file that has the correct data

with open(tbd_data_path) as csv_file:
  with open(ufactors_data_path) as json_file:
    ufactors_json = json.load(json_file)
    for row in csv.DictReader(csv_file):
      wall    = row["wall_reference"]
      type    = row["construction_type"]
      ufactor = float(row["u_w_per_m_k"])

      if wall in ufactors_json:
        print(f"Wall: {wall}\nConstruction Type: {type}", end="")
        ufactor_correct = ufactors_json[wall][type]
        if ufactor_correct == ufactor:
          print(f" CORRECT: U-Factor: {ufactor}\n")
        else:
          print(f" INCORRECT:\n  U-Factor (Denis): {ufactor_correct}\n  U-Factor (Volta): {ufactor}\n")
      else:
        print(f"Not Defined: {wall}\n")

# 3 incorrect entries as of 2025/11/19:
#   Wall: BTAP-ExteriorWall-WoodFramed-7 good
#   Construction Type: parapet INCORRECT:
#     U-Factor (Denis): 0.05
#     U-Factor (Volta): 0.07
#   Wall: BTAP-ExteriorWall-SteelFramed-2 good
#   Construction Type: parapet INCORRECT:
#     U-Factor (Denis): 0.1
#     U-Factor (Volta): 0.35
#   Wall: BTAP-ExteriorWall-SteelFramed-1 good
#   Construction Type: parapet INCORRECT:
#     U-Factor (Denis): 0.35
#     U-Factor (Volta): 0.1
