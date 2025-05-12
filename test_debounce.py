import threading
import time
from typing import Callable, Any

def debounce(func: Callable, wait: float):
    state = {'timeout': None}
    
    def executed_function(*args, **kwargs):
        def later():
            state['timeout'] = None
            func(*args, **kwargs)
        
        if state['timeout'] is not None:
            state['timeout'].cancel()
        
        state['timeout'] = threading.Timer(wait, later)
        state['timeout'].start()
    
    return executed_function

# Test function that prints when it's called
def test_function(query: str):
    print(f"Function called with: {query} at {time.time()}")

# Create a debounced version that waits 0.5 seconds
debounced_test = debounce(test_function, 0.5)

print("Testing debounce function...")
print("Calling function multiple times quickly (should only execute once):")

# Call the function multiple times in quick succession
debounced_test("first call")
time.sleep(0.1)  # Wait 0.1 seconds
debounced_test("second call")
time.sleep(0.1)  # Wait 0.1 seconds
debounced_test("third call")

print("\nWaiting for function to execute...")
time.sleep(1)  # Wait for the debounced function to execute

print("\nCalling function again after waiting (should execute):")
debounced_test("new call")

print("\nWaiting for final execution...")
time.sleep(1)  # Wait for the final call to execute 