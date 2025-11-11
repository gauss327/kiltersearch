import pandas as pd
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
import re
import json
from utils import compute_hull_area, mst_longest_edges, mst_average_edge

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
                hold_quality = None
                hold_grip_type = None
                for desc_key, desc_data in self.hold_descriptions.items():
                    if desc_data.get('x') == hold_x and desc_data.get('y') == hold_y:
                        hold_description = desc_data.get('description', '')
                        hold_quality = desc_data.get('quality', '')
                        hold_grip_type = desc_data.get('grip_type', '')
                        break
                
                holds.append({
                    'coordinate': hold_data.iloc[0]['name'],  # Grid position (e.g. "32,13" means 32nd hold from left, 13th hold up)
                    'x': hold_x,  # Physical x position in inches
                    'y': hold_y,  # Physical y position in inches
                    'role_id': role_id,
                    'role_name': hold_data.iloc[0]['role_name'],
                    'description': hold_description,  # Hold description from hold_descriptions.json
                    'quality': hold_quality,  # Hold quality from hold_descriptions.json
                    'grip_type': hold_grip_type  # Hold grip type from hold_descriptions.json
                })
        
        return holds
    
    def count_problem_holds(self, holds: List[Dict]) -> Dict:
        """Count the number of handholds and footholds in a problem."""
        handholds = [h for h in holds if h.get('role_name') in ['start', 'middle', 'finish']]
        footholds = [h for h in holds if h.get('role_name') == 'foot']
        
        return {
            "number_handholds": len(handholds),
            "number_footholds": len(footholds)
        }
    
    def calculate_problem_metrics(self, handholds: List[Dict]) -> Dict:
        """Calculate spatial metrics for a problem using hull area analysis."""
        # Calculate convex hull area coverage (percentage) for handholds
        hull_area_coverage = compute_hull_area(handholds)
        
        return {
            "hull_area_coverage": hull_area_coverage
        }
    
    def calculate_mst_metrics(self, handholds: List[Dict]) -> Dict:
        """Calculate MST metrics for handholds to find longest edges."""
        # Extract x,y coordinates from handholds
        coords = [(hold['x'], hold['y']) for hold in handholds]
        
        # Get MST longest edges (just the longest one)
        mst_edges = mst_longest_edges(coords, top_k=1)
        
        # Get average edge length in MST
        average_edge_length = mst_average_edge(coords)
        
        # Extract the longest edge distance
        max_edge_distance = mst_edges[0][2] if mst_edges else 0.0
        
        return {
            "max_edge_distance": max_edge_distance,
            "average_edge_length": average_edge_length,
            "mst_edges": mst_edges
        }
    
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
    
    def convert_to_problem_format(self, problem: Dict) -> Dict:
        """Convert a problem to the standardized format."""
        # Get holds and their roles
        holds = self.get_problem_holds(problem['uuid'])
        
        # Count handholds and footholds
        hold_counts = self.count_problem_holds(holds)
        
        # Filter for handholds and footholds
        handholds = [h for h in holds if h.get('role_name') in ['start', 'middle', 'finish']]
        footholds = [h for h in holds if h.get('role_name') == 'foot']
        
        # Calculate spatial metrics on handholds
        handhold_metrics = self.calculate_problem_metrics(handholds)
        
        # Calculate MST metrics on handholds
        mst_metrics = self.calculate_mst_metrics(handholds)
        
        # Calculate spatial metrics on footholds
        foothold_metrics = self.calculate_problem_metrics(footholds)
        
        # Get problem statistics for all angles
        problem_stats = self.get_problem_stats(problem['uuid'])
        
        # Convert holds to ensure JSON serializable types
        serializable_holds = []
        for hold in holds:
            serializable_holds.append({
                "coordinate": str(hold['coordinate']),
                "x": int(hold['x']) if hold['x'] is not None else 0,
                "y": int(hold['y']) if hold['y'] is not None else 0,
                "role": str(hold.get('role_name', 'middle')),
                "description": str(hold.get('description', '')),
                "quality": str(hold.get('quality', '')),
                "grip_type": str(hold.get('grip_type', ''))
            })
        
        # Create the standardized format with just the basic fields filled
        return {
            
            "metadata": {
                "id": str(problem['uuid']),
                "name": str(problem['name']),
                "setter": str(problem.get('setter_username', 'Unknown')),
                "problem_variants": problem_stats
            },
            
            "board": {
                "width_cols": 20,
                "height_rows": 35,
                "angle_deg": int(problem.get('angle', 0)) if problem.get('angle') is not None else 0
            },
            
            "holds": serializable_holds,
            
            "grip_list": [hold["grip_type"].upper() for hold in serializable_holds if hold["grip_type"]],
            
            "metrics": {
                "number_handholds": hold_counts["number_handholds"],
                "number_footholds": hold_counts["number_footholds"],
                "hold_hand_density": handhold_metrics["hull_area_coverage"]/hold_counts["number_handholds"] if hold_counts["number_handholds"] > 0 else 0.0, 
                "hold_foot_density": foothold_metrics["hull_area_coverage"]/hold_counts["number_footholds"] if hold_counts["number_footholds"] > 0 else 0.0, 
                "hull_area_coverage": handhold_metrics["hull_area_coverage"],
                "hull_area_coverage_feet": foothold_metrics["hull_area_coverage"],
                "max_edge_distance": mst_metrics["max_edge_distance"],
                "average_edge_length": mst_metrics["average_edge_length"],
            },
            
            #tags below will be AI generated 
            "style": {
                "style_tags": [],
                "notes": [],
                "feet_context": ""
            },
            
            "summary": "",
            
            "embedding": {
                "fused_text": "",
                "control_text": "",
                "semantic_text": ""
            },
            
        }
    
    def process_all_problems(self, problems: List[Dict]) -> pd.DataFrame:
        """Process all problems and return a DataFrame."""
        processed_problems = [self.process_problem(p) for p in problems]
        return pd.DataFrame(processed_problems)

def main():
    # Example usage
    db_path = Path("data/raw/db.sqlite3")
    hold_descriptions_path = Path("data/hold_descriptions.json")
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
    
    # Convert problems to standardized format
    converted_problems = []
    for problem in problems:
        try:
            converted = processor.convert_to_problem_format(problem)
            converted_problems.append(converted)
        except Exception as e:
            print(f"Error converting problem {problem.get('name', 'Unknown')}: {e}")
            continue
    
    # Save converted problems to JSON
    output_path = Path("data/processed/converted_problems.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(converted_problems, f, indent=2)
    
    print(f"Converted {len(converted_problems)} problems to standardized format")
    print(f"Saved to: {output_path}")
    
    # Print first problem as example
    if converted_problems:
        print("\nExample converted problem:")
        print(json.dumps(converted_problems[0], indent=2))

if __name__ == "__main__":
    main() 