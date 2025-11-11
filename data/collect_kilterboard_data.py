import sqlite3
import pandas as pd
from typing import Dict, List
import json
from pathlib import Path

# Get the absolute path to the database
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR / "data" / "raw" / "db.sqlite3"

def fetch_kilterboard_data(db_path: str = str(DB_PATH)) -> List[Dict]:
    """
    Fetch Kilterboard problem data from the local SQLite database.
    Args:
        db_path: Path to the SQLite database file
    Returns:
        List of dictionaries containing problem information
    """
    problems = []
    try:
        # Connect to the SQLite database
        print(f"Connecting to database at: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Query the climbs table with actual columns
        cursor.execute("""
            SELECT 
                uuid,
                name,
                description,
                hsm,
                edge_left,
                edge_right,
                edge_bottom,
                edge_top,
                angle,
                frames_count,
                frames_pace,
                frames,
                is_draft,
                is_listed,
                created_at
            FROM climbs
        """)
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        print(f"Found columns: {columns}")
        
        # Fetch all problems
        rows = cursor.fetchall()
        print(f"Found {len(rows)} rows")
        
        for row in rows:
            problem = dict(zip(columns, row))
            problems.append(problem)
            
    except sqlite3.Error as e:
        print(f"Error accessing database: {e}")
        return []
    finally:
        if conn:
            conn.close()
    
    return problems

def process_problem_data(problems: List[Dict]) -> pd.DataFrame:
    """
    Process the raw problem data into a structured format.
    Args:
        problems: List of dictionaries containing raw problem data
    Returns:
        DataFrame with processed problem data
    """
    # Convert to DataFrame
    df = pd.DataFrame(problems)
    
    # Create a text field for embedding
    df['text_for_embedding'] = df.apply(lambda row: 
        f"Problem: {row['name']}. "
        f"Description: {row['description']}. "
        f"Setter: {row['setter_username']}. "
        f"Wall angle: {row['angle']} degrees. "
        f"Problem bounds: left {row['edge_left']}, right {row['edge_right']}, "
        f"bottom {row['edge_bottom']}, top {row['edge_top']}",
        axis=1
    )
    
    return df

def save_data(df: pd.DataFrame, output_path: Path) -> None:
    """
    Save the processed data to a file.
    Args:
        df: Processed DataFrame
        output_path: Path to save the data
    """
    # Save as CSV
    df.to_csv(output_path, index=False)

def main():
    # Create output directories if they don't exist
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    # Fetch and process data
    problems = fetch_kilterboard_data()
    
    # Save raw data for inspection
    with open(raw_dir / "raw_problems.json", "w") as f:
        json.dump(problems, f, indent=2)
    
    df = process_problem_data(problems)
    
    # Save processed data
    save_data(df, processed_dir / "kilterboard_problems.csv")

if __name__ == "__main__":
    main() 