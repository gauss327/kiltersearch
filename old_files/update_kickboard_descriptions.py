import json
from pathlib import Path

def update_kickboard_descriptions():
    # Read the current descriptions
    with open('data/hold_descriptions_old.json', 'r') as f:
        hold_descriptions = json.load(f)
    
    # Update descriptions for KB1 and KB2 holds
    for placement_id, data in hold_descriptions.items():
        if 'KB1' in data['hole_name']:
            data['description'] = "lower kickboard foothold. enough to put pressure on but not great"
            data['type'] = "foot"
        elif 'KB2' in data['hole_name']:
            data['description'] = "higher kickboard foothold. slightly larger footholds"
            data['type'] = "foot"
    
    # Write back to file
    with open('data/hold_descriptions_old.json', 'w') as f:
        json.dump(hold_descriptions, f, indent=4)
    
    print("Updated kickboard hold descriptions")

if __name__ == "__main__":
    update_kickboard_descriptions() 