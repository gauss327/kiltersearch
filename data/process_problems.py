import pandas as pd
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
import re
import json

class ProblemProcessor:
    def __init__(self, db_path: Path, hold_descriptions_path: Path = None):
        """Initialize the processor with database connection."""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        
        # Load hold descriptions if path provided
        self.hold_descriptions = {}
        if hold_descriptions_path and hold_descriptions_path.exists():
            with open(hold_descriptions_path, 'r') as f:
                self.hold_descriptions = json.load(f)
        
    def __del__(self):
        """Clean up database connection."""
        if hasattr(self, 'conn'):
            self.conn.close()
            
    def get_problem_holds(self, climb_uuid: str) -> List[Dict]:
        """Get all holds used in a problem from the frames data."""
        # Get the frames data
        query = "SELECT frames FROM climbs WHERE uuid = ?"
        frames = pd.read_sql_query(query, self.conn, params=(climb_uuid,)).iloc[0]['frames']
        
        # Parse frames data (format: p{placement_id}r{role_id})
        holds = []
        for match in re.finditer(r'p(\d+)r(\d+)', frames):
            placement_id = match.group(1)
            role_id = match.group(2)
            
            # Get hold details through placements table
            hold_query = """
            SELECT h.name, h.x, h.y, h.product_id, pr.name as role_name
            FROM placements p
            JOIN holes h ON p.hole_id = h.id
            LEFT JOIN placement_roles pr ON pr.id = ? AND pr.product_id = h.product_id
            WHERE p.id = ?
            """
            hold_data = pd.read_sql_query(hold_query, self.conn, params=(role_id, placement_id))
            
            if not hold_data.empty:
                hold_x = hold_data.iloc[0]['x']
                hold_y = hold_data.iloc[0]['y']
                
                # Find matching hold description by x, y coordinates
                hold_description = None
                for desc_key, desc_data in self.hold_descriptions.items():
                    if desc_data.get('x') == hold_x and desc_data.get('y') == hold_y:
                        hold_description = desc_data.get('description', '')
                        break
                
                holds.append({
                    'coordinate': hold_data.iloc[0]['name'],  # Grid position (e.g. "32,13" means 32nd hold from left, 13th hold up)
                    'x': hold_x,  # Physical x position in inches
                    'y': hold_y,  # Physical y position in inches
                    'role_id': role_id,
                    'role_name': hold_data.iloc[0]['role_name'],
                    'description': hold_description  # Hold description from hold_descriptions.json
                })
        
        return holds
    
    def get_problem_stats(self, climb_uuid: str) -> Dict:
        """Get statistics for a problem."""
        query = """
        SELECT 
            angle,
            display_difficulty,
            ascensionist_count,
            quality_average,
            fa_username,
            fa_at
        FROM climb_stats
        WHERE climb_uuid = ?
        """
        return pd.read_sql_query(query, self.conn, params=(climb_uuid,)).to_dict('records')
    
    def process_problem(self, problem: Dict) -> Dict:
        """Process a single problem with all its related data."""
        # Get holds and their roles
        holds = self.get_problem_holds(problem['uuid'])
        
        # Get problem statistics
        stats = self.get_problem_stats(problem['uuid'])
        
        return {
            'uuid': problem['uuid'],
            'name': problem['name'],
            'description': problem['description'],
            'setter': problem['setter_username'],
            'angle': problem['angle'],
            'holds': holds,
            'stats': stats
        }
    
    def process_all_problems(self, problems: List[Dict]) -> pd.DataFrame:
        """Process all problems and return a DataFrame."""
        processed_problems = [self.process_problem(p) for p in problems]
        return pd.DataFrame(processed_problems)

def main():
    # Example usage
    db_path = Path("raw/db.sqlite3")
    hold_descriptions_path = Path("hold_descriptions.json")
    processor = ProblemProcessor(db_path, hold_descriptions_path)
    
    # Get problems with high ascensionist counts
    query = """
    SELECT c.* 
    FROM climbs c
    JOIN climb_stats cs ON c.uuid = cs.climb_uuid
    WHERE cs.ascensionist_count > 1000
    ORDER BY cs.ascensionist_count DESC
    LIMIT 5
    """
    problems = pd.read_sql_query(query, processor.conn).to_dict('records')
    
    # Process them
    processed_df = processor.process_all_problems(problems)
    
    # Print detailed info for each problem
    for idx, problem in processed_df.iterrows():
        print(f"\nProblem {idx + 1} Details:")
        print(f"Name: {problem['name']}")
        print(f"Setter: {problem['setter']}")
        print(f"Angle: {problem['angle']}")
        
        print("\nRaw Climb Data:")
        for key, value in problems[idx].items():
            print(f"{key}: {value}")
        
        print("\nHolds:")
        for hold in problem['holds']:
            print(f"- {hold}")
            
        print("\nStats:")
        for stat in problem['stats']:
            print(f"- {stat}")
        print("\n" + "="*50)  # Separator between problems

if __name__ == "__main__":
    main() 