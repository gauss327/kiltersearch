import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np
import json

def load_data(input_path: Path) -> pd.DataFrame:
    """Load the processed problem data."""
    return pd.read_csv(input_path)

def generate_embeddings(df: pd.DataFrame) -> dict:
    """
    Generate embeddings for each problem using sentence-transformers.
    Returns a dictionary mapping problem UUIDs to their embeddings.
    """
    # Initialize the model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Generate embeddings for all problems
    texts = df['text_for_embedding'].tolist()
    embeddings = model.encode(texts)
    
    # Create a dictionary mapping UUIDs to embeddings
    embeddings_dict = {
        uuid: embedding.tolist() 
        for uuid, embedding in zip(df['uuid'], embeddings)
    }
    
    return embeddings_dict

def save_embeddings(embeddings: dict, output_path: Path) -> None:
    """Save the embeddings to a JSON file."""
    with open(output_path, 'w') as f:
        json.dump(embeddings, f)

def main():
    # Set up paths
    processed_dir = Path("data/processed")
    embeddings_dir = Path("data/embeddings")
    embeddings_dir.mkdir(parents=True, exist_ok=True)
    
    # Load the processed data
    print("Loading processed data...")
    df = load_data(processed_dir / "kilterboard_problems.csv")
    
    # Generate embeddings
    print("Generating embeddings...")
    embeddings = generate_embeddings(df)
    
    # Save embeddings
    print("Saving embeddings...")
    save_embeddings(embeddings, embeddings_dir / "problem_embeddings.json")
    
    print("Done!")

if __name__ == "__main__":
    main() 