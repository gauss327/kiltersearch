// Get references to the search input and results container
const searchInput = document.getElementById('searchInput');
const resultsDiv = document.getElementById('results');

// Function to prevent too many rapid searches
// It waits 300ms after the user stops typing before searching
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Function to perform the search
async function search(query) {
    // Clear results if query is empty
    if (!query) {
        resultsDiv.innerHTML = '';
        return;
    }

    try {
        // Send request to our Flask backend
        const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
        const results = await response.json();
        
        // Create HTML for each result
        resultsDiv.innerHTML = results.map(result => `
            <div class="result">
                <div class="name">${result.name}</div>
                <div class="setter">Setter: ${result.setter}</div>
                <div class="similarity">Similarity: ${result.similarity.toFixed(3)}</div>
                <div class="description">${result.description || 'No description'}</div>
            </div>
        `).join('');
    } catch (error) {
        // Show error message if something goes wrong
        console.error('Error:', error);
        resultsDiv.innerHTML = '<div>Error searching. Please try again.</div>';
    }
}

// Set up the search to run when user types
const debouncedSearch = debounce(search, 300);
searchInput.addEventListener('input', (e) => debouncedSearch(e.target.value)); 