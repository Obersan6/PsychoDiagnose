// Autocomplete functionality for search bars in categories, disorders, signs, and symptoms.
// Fetches and displays suggestions dynamically as the user types in the input field.


async function setupAutocomplete(inputId, suggestionsContainerId, endpoint) {
    const input = document.getElementById(inputId);
    const suggestionsContainer = document.getElementById(suggestionsContainerId);

    // Exit early if the input field or suggestions container doesn't exist
    if (!input || !suggestionsContainer) {
        console.warn(`Autocomplete setup skipped: Element(s) not found for inputId: ${inputId} or suggestionsContainerId: ${suggestionsContainerId}`);
        return;
    }

    let suggestions = [];
    let selectedIndex = -1;
    let isInteractingWithSuggestions = false;

    // Fetch and display suggestions when the user types
    input.addEventListener('input', async () => {
        const query = input.value.trim();

        // Reset suggestions and index
        suggestions = [];
        selectedIndex = -1;
        suggestionsContainer.innerHTML = '';

        if (!query) return;

        try {
            // Fetch matching suggestions
            const response = await fetch(`${endpoint}?query=${encodeURIComponent(query)}`);
            if (!response.ok) throw new Error(`Error: ${response.statusText}`);
            
             // Parse the JSON response containing suggestions
            suggestions = await response.json();

            // Populate suggestions
            suggestions.forEach((suggestion, index) => {
                const suggestionItem = document.createElement('div');
                suggestionItem.textContent = suggestion;
                suggestionItem.classList.add('suggestion-item');
                suggestionItem.dataset.index = index;

                // Handle click on suggestion
                suggestionItem.addEventListener('mousedown', () => {
                    isInteractingWithSuggestions = true; // Mark interaction
                    input.value = suggestion; // Set input value to selected suggestion
                    suggestionsContainer.innerHTML = ''; // Clear suggestions
                    input.form.submit(); // Submit the form
                });

                suggestionsContainer.appendChild(suggestionItem);
            });
        } catch (error) {
            console.error(`Autocomplete error: ${error}`);
        }
    });

    // Handle keyboard navigation and selection
    input.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
            e.preventDefault();
            if (e.key === 'ArrowDown') {
                selectedIndex = (selectedIndex + 1) % suggestions.length;
            } else if (e.key === 'ArrowUp') {
                selectedIndex = (selectedIndex - 1 + suggestions.length) % suggestions.length;
            }
            updateSuggestionHighlight(suggestionsContainer, selectedIndex); // Highlight the selection
        } else if (e.key === 'Enter') {
            e.preventDefault(); // Prevent form submission on Enter
            if (selectedIndex >= 0) {
                input.value = suggestions[selectedIndex]; // Use selected suggestion
                suggestionsContainer.innerHTML = ''; // Clear suggestions
                input.form.submit(); // Submit the form
            }
        }
    });

    // Clear suggestions when input loses focus (delayed to allow click events)
    input.addEventListener('blur', () => {
        if (!isInteractingWithSuggestions) {
            setTimeout(() => (suggestionsContainer.innerHTML = ''), 100);
        }
        isInteractingWithSuggestions = false; // Reset interaction flag
    });
}

// Highlight the currently selected suggestion
function updateSuggestionHighlight(container, index) {
    const items = container.querySelectorAll('.suggestion-item');
    items.forEach((item, idx) => {
        item.classList.toggle('highlighted', idx === index); // Highlight the selected item
    });
}

// Apply the autocomplete function to pecific search inputs and endpoints
setupAutocomplete('search_category', 'suggestions-category', '/categories/autocomplete');
setupAutocomplete('search_disorder', 'suggestions-disorder', '/disorders/autocomplete');
setupAutocomplete('search_sign', 'suggestions-sign', '/signs/autocomplete');
setupAutocomplete('search_symptom', 'suggestions-symptom', '/symptoms/autocomplete');





