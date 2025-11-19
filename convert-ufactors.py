# ***CoPilot generated file, verify if this is correct later

import json
import re

# Read the Ruby-like data from file
with open('ufactors.txt', 'r') as f:
    content = f.read()

# Define the key mappings
key_mappings = {
    'MASS2_BAD': 'BTAP-ExteriorWall-Mass-2 bad',
    'MASS2_GOOD': 'BTAP-ExteriorWall-Mass-2 good',
    'MASSB_BAD': 'BTAP-ExteriorWall-Mass-2b bad',
    'MASSB_GOOD': 'BTAP-ExteriorWall-Mass-2b good',
    'MASS4_BAD': 'BTAP-ExteriorWall-Mass-4 bad',
    'MASS4_GOOD': 'BTAP-ExteriorWall-Mass-4 good',
    'MASS8_BAD': 'BTAP-ExteriorWall-Mass-8c bad',
    'MASS8_GOOD': 'BTAP-ExteriorWall-Mass-8c good',
    'WOOD5_BAD': 'BTAP-ExteriorWall-WoodFramed-5 bad',
    'WOOD5_GOOD': 'BTAP-ExteriorWall-WoodFramed-5 good',
    'WOOD7_BAD': 'BTAP-ExteriorWall-WoodFramed-7 bad',
    'WOOD7_GOOD': 'BTAP-ExteriorWall-WoodFramed-7 good',
    'STEL1_BAD': 'BTAP-ExteriorWall-SteelFramed-1 bad',
    'STEL1_GOOD': 'BTAP-ExteriorWall-SteelFramed-1 good',
    'STEL2_BAD': 'BTAP-ExteriorWall-SteelFramed-2 bad',
    'STEL2_GOOD': 'BTAP-ExteriorWall-SteelFramed-2 good',
}

# Parse the data
result = {}
lines = content.split('\n')

for line in lines:
    # Match lines like: d[MASS2][ :bad][:rimjoist    ] = { psi: 0.470 }
    match = re.match(r'd\[(\w+)\]\[\s*:(\w+)\]\[:(\w+)\s*\]\s*=\s*{\s*psi:\s*([\d.]+)\s*}', line)
    
    if match:
        prefix, quality, edge_type, psi_value = match.groups()
        
        # Skip :id entries and non-BAD/GOOD entries
        if edge_type == 'id':
            continue
        
        # Create the key from prefix and quality
        key_suffix = f"{prefix}_{quality.upper()}"
        
        # Check if this key exists in our mappings
        if key_suffix in key_mappings:
            full_key = key_mappings[key_suffix]
            
            # Initialize the entry if it doesn't exist
            if full_key not in result:
                result[full_key] = {}
            
            # Add the edge type with its value (remove 'psi:' wrapper)
            result[full_key][edge_type] = float(psi_value)

# Output as formatted JSON
output = json.dumps(result, indent=2, sort_keys=True)
print(output)

# Also save to file
with open('ufactors_converted.json', 'w') as f:
    f.write(output)

print("\n✓ Converted data saved to ufactors_converted.json")
