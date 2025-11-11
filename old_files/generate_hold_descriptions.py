import sqlite3
import json
from pathlib import Path
import pandas as pd

def generate_hold_descriptions():
    # Connect to database
    db_path = Path("data/raw/db.sqlite3")
    conn = sqlite3.connect(db_path)
    
    # Get all placements for layout_id 1
    query = """
    SELECT 
        p.id as placement_id,
        p.layout_id,
        p.hole_id,
        p.set_id,
        p.default_placement_role_id,
        h.name as hole_name,
        h.x,
        h.y
    FROM placements p
    JOIN holes h ON p.hole_id = h.id
    WHERE p.layout_id = 1
    """
    
    # Execute query and convert to list of dictionaries
    placements = pd.read_sql_query(query, conn).to_dict('records')
    
    # Create hold descriptions dictionary
    hold_descriptions = {}
    for p in placements:
        hold_descriptions[str(p['placement_id'])] = {
            "placement_id": p['placement_id'],
            "layout_id": p['layout_id'],
            "hole_id": p['hole_id'],
            "set_id": p['set_id'],
            "default_placement_role_id": p['default_placement_role_id'],
            "hole_name": p['hole_name'],
            "x": p['x'],
            "y": p['y'],
            "orientation": None,  # Will be one of: facing_up, facing_down, facing_left, facing_right, angled_up_left, flat_to_wall
            "description": ""  # To be filled in manually
        }
    
    # Write to JSON file
    output_path = Path("data/hold_descriptions_old.json")
    with open(output_path, 'w') as f:
        json.dump(hold_descriptions, f, indent=4)
    
    print(f"Generated hold descriptions for {len(hold_descriptions)} holds")
    print(f"Output written to {output_path}")

if __name__ == "__main__":
    generate_hold_descriptions() 