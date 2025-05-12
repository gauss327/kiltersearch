from flask import Flask, render_template, request, jsonify
from pathlib import Path
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd

app = Flask(__name__)

# Get the absolute path to the project root
PROJECT_ROOT = Path(__file__).parent

# Simple paths without nesting
embeddings_path = PROJECT_ROOT / "data" / "embeddings" / "problem_embeddings.json"
problems_path = PROJECT_ROOT / "data" / "processed" / "kilterboard_problems.csv"

# Load data
print("Loading embeddings and problems...")
print(f"Looking for embeddings at: {embeddings_path}")
print(f"Looking for problems at: {problems_path}")

with open(embeddings_path, 'r') as f:
    embeddings = json.load(f)
problems_df = pd.read_csv(problems_path)

# Initialize model
model = SentenceTransformer('all-MiniLM-L6-v2')

def search_problems(query: str, top_k: int = 5) -> list:
    """Search for problems using the query."""
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
    results = sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]
    
    # Format results
    formatted_results = []
    for uuid, similarity in results:
        problem = problems_df[problems_df['uuid'] == uuid].iloc[0]
        # Convert NaN to None for JSON serialization
        description = problem['description'] if pd.notna(problem['description']) else None
        formatted_results.append({
            'uuid': uuid,
            'similarity': float(similarity),
            'name': problem['name'],
            'setter': problem['setter_username'],
            'description': description
        })
    
    return formatted_results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    results = search_problems(query)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 