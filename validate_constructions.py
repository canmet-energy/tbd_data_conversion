#!/usr/bin/env python3
"""
Validate construction JSON files against source Excel data

This script checks that:
1. All constructions from Excel appear in JSON
2. All PSI values from Excel are present in JSON
3. Material layer IDs match between Excel and JSON
4. Layer counts match for each construction/PSI combination
"""

# Human: copilot made this errors are cause of the replaced fibreglass entries,
#        should only be 2 mismatches in GlassDoor and 6 in ExteriorWindow

import json
import sys
from pathlib import Path
import pandas as pd
import common


def validate_construction_file(file_path, sheet_name):
    """
    Validate JSON file against Excel source data.
    
    Returns:
        tuple: (is_valid, list of errors, list of warnings, stats)
    """
    errors = []
    warnings = []
    stats = {
        "excel_constructions": 0,
        "json_constructions": 0,
        "excel_psi_values": 0,
        "json_psi_values": 0,
        "matched": 0,
        "mismatched": 0
    }
    
    if not file_path.exists():
        errors.append(f"JSON file not found: {file_path}")
        return False, errors, warnings, stats
    
    # Load Excel data
    try:
        df = pd.read_excel(common.SHEET_DATA_PATH, sheet_name=sheet_name)
    except Exception as e:
        errors.append(f"Failed to load Excel sheet '{sheet_name}': {e}")
        return False, errors, warnings, stats
    
    # Load JSON data
    try:
        with open(file_path, 'r') as f:
            json_data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in {file_path}: {e}")
        return False, errors, warnings, stats
    
    id_column = common.CONSTRUCTION_ID_MAP[sheet_name]
    
    # Forward fill Excel data
    df["construction_type_name"] = df["construction_type_name"].ffill()
    df["u_w_per_m2_k"] = df["u_w_per_m2_k"].ffill()
    df["u_w_per_m2_k"] = df["u_w_per_m2_k"].round(3)
    
    # Create MultiIndex for comparison
    df = df.set_index(["construction_type_name", "u_w_per_m2_k"])
    
    # Get unique constructions and PSI values from Excel
    excel_constructions = set(df.index.get_level_values(0).unique())
    stats["excel_constructions"] = len(excel_constructions)
    
    json_constructions = set(json_data.keys())
    stats["json_constructions"] = len(json_constructions)
    
    # Check for missing constructions
    missing_in_json = excel_constructions - json_constructions
    if missing_in_json:
        for construction in missing_in_json:
            errors.append(f"Construction '{construction}' found in Excel but not in JSON")
    
    extra_in_json = json_constructions - excel_constructions
    if extra_in_json:
        for construction in extra_in_json:
            warnings.append(f"Construction '{construction}' found in JSON but not in Excel")
    
    # Validate each construction and PSI combination
    for (construction, psi), group in df.groupby(level=[0, 1]):
        psi_str = str(psi)
        stats["excel_psi_values"] += 1
        
        if construction not in json_data:
            continue
        
        if "psi" not in json_data[construction]:
            errors.append(f"{construction}: Missing 'psi' key in JSON")
            continue
        
        json_psi_dict = json_data[construction]["psi"]
        
        # Check if PSI value exists in JSON (try both float and string)
        json_psi_data = None
        if psi_str in json_psi_dict:
            json_psi_data = json_psi_dict[psi_str]
        elif psi in json_psi_dict:
            json_psi_data = json_psi_dict[psi]
        
        if json_psi_data is None:
            errors.append(f"{construction}: PSI value {psi} from Excel not found in JSON")
            stats["mismatched"] += 1
            continue
        
        # Validate material layers
        if id_column not in json_psi_data:
            errors.append(f"{construction} [PSI={psi}]: Missing '{id_column}' in JSON")
            stats["mismatched"] += 1
            continue
        
        json_layers = json_psi_data[id_column]
        excel_layer_ids = [int(x) for x in group[id_column].dropna().tolist()]
        json_layer_ids = [int(layer["id"]) for layer in json_layers]
        
        # Compare layer counts
        if len(excel_layer_ids) != len(json_layer_ids):
            errors.append(
                f"{construction} [PSI={psi}]: Layer count mismatch - "
                f"Excel has {len(excel_layer_ids)} layers, JSON has {len(json_layer_ids)} layers"
            )
            stats["mismatched"] += 1
            continue
        
        # Compare layer IDs
        if excel_layer_ids != json_layer_ids:
            errors.append(
                f"{construction} [PSI={psi}]: Layer IDs mismatch - "
                f"Excel: {excel_layer_ids}, JSON: {json_layer_ids}"
            )
            stats["mismatched"] += 1
        else:
            stats["matched"] += 1
    
    # Count JSON PSI values
    for construction_data in json_data.values():
        if "psi" in construction_data:
            stats["json_psi_values"] += len(construction_data["psi"])
    
    return len(errors) == 0, errors, warnings, stats


def main():
    """Main validation function."""
    print("="*80)
    print("CONSTRUCTION JSON vs EXCEL VALIDATION")
    print("="*80)
    
    all_valid = True
    total_stats = {
        "excel_constructions": 0,
        "json_constructions": 0,
        "excel_psi_values": 0,
        "json_psi_values": 0,
        "matched": 0,
        "mismatched": 0
    }
    
    for sheet_name, file_name in common.CONSTRUCTION_PAIRS:
        file_path = Path(file_name)
        print(f"\nValidating: {file_name} vs Excel sheet '{sheet_name}'")
        print("-" * 80)
        
        is_valid, errors, warnings, stats = validate_construction_file(file_path, sheet_name)
        
        # Update totals
        for key in total_stats:
            total_stats[key] += stats[key]
        
        # Print stats
        print(f"  Excel Constructions: {stats['excel_constructions']}")
        print(f"  JSON Constructions:  {stats['json_constructions']}")
        print(f"  Excel PSI Values:    {stats['excel_psi_values']}")
        print(f"  JSON PSI Values:     {stats['json_psi_values']}")
        print(f"  Matched:             {stats['matched']}")
        print(f"  Mismatched:          {stats['mismatched']}")
        
        if warnings:
            print(f"\n  ⚠ Warnings ({len(warnings)}):")
            for warning in warnings[:10]:
                print(f"    - {warning}")
            if len(warnings) > 10:
                print(f"    ... and {len(warnings) - 10} more warnings")
        
        if errors:
            print(f"\n  ✗ Errors ({len(errors)}):")
            for error in errors[:10]:
                print(f"    - {error}")
            if len(errors) > 10:
                print(f"    ... and {len(errors) - 10} more errors")
            all_valid = False
        else:
            print("\n  ✓ Validation passed")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total Excel Constructions: {total_stats['excel_constructions']}")
    print(f"Total JSON Constructions:  {total_stats['json_constructions']}")
    print(f"Total Excel PSI Values:    {total_stats['excel_psi_values']}")
    print(f"Total JSON PSI Values:     {total_stats['json_psi_values']}")
    print(f"Total Matched:             {total_stats['matched']}")
    print(f"Total Mismatched:          {total_stats['mismatched']}")
    
    if all_valid:
        print("\n✓ All construction files match Excel data!")
        print("="*80)
        sys.exit(0)
    else:
        print("\n✗ Validation failed with errors")
        print("="*80)
        sys.exit(1)


if __name__ == '__main__':
    main()
