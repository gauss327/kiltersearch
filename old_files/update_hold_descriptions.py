import json
import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Callable
from hold_orientations import ORIENTATION_MAPPINGS

def update_hold_descriptions(rules: List[Dict]):
    """
    Update hold descriptions based on a list of rules.
    Each rule should be a dict with:
    - 'condition': function that takes hold data and returns True if rule should apply
    - 'updates': dict of fields to update and their values
    """
    # Read the current descriptions
    with open('data/hold_descriptions.json', 'r') as f:
        hold_descriptions = json.load(f)
    
    # Connect to database
    conn = sqlite3.connect('data/raw/db.sqlite3')
    
    # Get coordinates and hole_id for each hold using the same query as process_problems.py
    for placement_id, data in hold_descriptions.items():
        hold_query = """
        SELECT h.id as hole_id, h.name, h.x, h.y, h.product_id
        FROM placements p
        JOIN holes h ON p.hole_id = h.id
        WHERE p.id = ?
        """
        hold_data = pd.read_sql_query(hold_query, conn, params=(placement_id,))
        
        if not hold_data.empty:
            data['hole_name'] = int(hold_data.iloc[0]['hole_id'])  # Use the integer hole_id
            data['coordinate'] = hold_data.iloc[0]['name']  # Grid position
            data['x'] = int(hold_data.iloc[0]['x'])  # Physical x position in inches
            data['y'] = int(hold_data.iloc[0]['y'])  # Physical y position in inches
            #data['grip_type'] = None
            #data['quality'] = None
            #data['orientation'] = None
           # data['description'] = None
    
    conn.close()
    
    # Apply each rule to all holds
    for placement_id, data in hold_descriptions.items():
        for rule in rules:
            if rule['condition'](data):
                data.update(rule['updates'])
    
    # Write back to file
    with open('data/hold_descriptions_old.json', 'w') as f:
        json.dump(hold_descriptions, f, indent=4)
    
    print("Updated hold descriptions")

if __name__ == "__main__":
    # Define rules for updating descriptions
    rules = [
        # Rule for KB1 holds
        {
            'condition': lambda data: 'KB1' in data['coordinate'],
            'updates': {
                'grip_type': 'foot',
                'quality': 'poor',
                'description': "lower kickboard foothold. enough to put pressure on but not great"
            }
        },
        # Rule for KB2 holds
        {
            'condition': lambda data: 'KB2' in data['coordinate'],
            'updates': {
                'grip_type': 'foot',
                'quality': 'medium',
                'description': "higher kickboard foothold. slightly larger footholds"
            }
        },
        # Rule for holds with odd first coordinate (excluding KB holds)
        {
            'condition': lambda data: (
                'KB' not in data['coordinate'] and 
                int(data['coordinate'].split(',')[0]) % 2 == 1
            ),
            'updates': {
                'grip_type': 'foot',
                'quality': 'poor',
                'description': "primarily a foothold. very bad handhold"
            }
        }
    ]
    
    update_hold_descriptions(rules) 