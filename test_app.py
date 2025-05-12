import requests
import time
import subprocess
import sys
from pathlib import Path

def start_flask_server():
    """Start the Flask server in a separate process."""
    flask_process = subprocess.Popen(
        [sys.executable, 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # Wait for server to start
    time.sleep(2)
    return flask_process

def test_search(query: str):
    """Test a search query."""
    try:
        response = requests.get(f'http://localhost:5000/search?q={query}')
        if response.status_code == 200:
            results = response.json()
            print(f"\nSearch results for '{query}':")
            for result in results:
                print(f"- {result['name']} (Similarity: {result['similarity']:.3f})")
        else:
            print(f"Error: Status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

def main():
    print("Starting Flask server...")
    flask_process = start_flask_server()
    
    try:
        # Test some searches
        test_searches = [
            "crimpy",          # Test hold type
            "slopers",         # Test another hold type
            "Andrew",          # Test setter name
            "45 degree",       # Test angle
            "dynamic move"     # Test movement type
        ]
        
        for query in test_searches:
            test_search(query)
            time.sleep(1)  # Wait between searches
            
    finally:
        # Clean up
        print("\nStopping Flask server...")
        flask_process.terminate()
        flask_process.wait()

if __name__ == "__main__":
    main() 