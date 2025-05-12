import json
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd

def load_embeddings(embeddings_path: Path) -> dict:
    """Load the problem embeddings."""
    with open(embeddings_path, 'r') as f:
        return json.load(f)

def load_problems(problems_path: Path) -> pd.DataFrame:
    """Load the problem data."""
    return pd.read_csv(problems_path)

def search_problems(query: str, embeddings: dict, model: SentenceTransformer, top_k: int = 5) -> list:
    """
    Search for problems using the query..
    Returns a list of (uuid, similarity_score) tuples.
    """
    # Convert query to embedding
    query_embedding = model.encode(query)
    
    # Calculate similarities
    similarities = []
    for uuid, problem_embedding in embeddings.items():
        similarity = np.dot(query_embedding, problem_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(problem_embedding)
        )
        similarities.append((uuid, similarity))
    
    # Sort by similarity and return top k
    return sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]

def main():
    # Set up paths
    embeddings_path = Path("data/embeddings/problem_embeddings.json")
    problems_path = Path("data/processed/kilterboard_problems.csv")
    
    # Load data
    print("Loading embeddings and problems...")
    embeddings = load_embeddings(embeddings_path)
    problems_df = load_problems(problems_path)
    
    # Initialize model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Interactive search loop
    while True:
        query = input("\nEnter your search query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
            
        # Search for problems
        results = search_problems(query, embeddings, model)
        
        # Display results
        print("\nTop matching problems:")
        for uuid, similarity in results:
            problem = problems_df[problems_df['uuid'] == uuid].iloc[0]
            print(f"\nSimilarity: {similarity:.3f}")
            print(f"Name: {problem['name']}")
            print(f"Setter: {problem['setter_username']}")
            print(f"Description: {problem['description']}")

if __name__ == "__main__":
    main() 