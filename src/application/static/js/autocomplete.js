// Autocomplete for category search input

// document.addEventListener("DOMContentLoaded", () => {
//     const searchInput = document.getElementById("search_query");
//     const suggestionsList = document.getElementById("suggestions-list");

//     async function fetchSuggestions(query) {
//         console.log(`Fetching suggestions for query: "${query}"`);
//         try {
//             const response = await fetch(`/categories/autocomplete?query=${encodeURIComponent(query)}`);
//             const suggestions = await response.json();
//             console.log("Suggestions received:", suggestions);
//             return suggestions;
//         } catch (error) {
//             console.error("Error fetching suggestions:", error);
//             return [];
//         }
//     }

//     function renderSuggestions(suggestions) {
//         console.log("Rendering suggestions:", suggestions);
//         suggestionsList.innerHTML = ""; // Clear previous suggestions

//         suggestions.forEach(suggestion => {
//             const suggestionItem = document.createElement("div");
//             suggestionItem.className = "suggestion-item";
//             suggestionItem.textContent = suggestion;

//             // Add click event to select the suggestion
//             suggestionItem.addEventListener("click", () => {
//                 searchInput.value = suggestion;
//                 suggestionsList.innerHTML = "";
//             });

//             suggestionsList.appendChild(suggestionItem);
//         });

//         // Show the suggestions container if there are suggestions
//         suggestionsList.style.display = suggestions.length > 0 ? "block" : "none";
//     }

//     searchInput.addEventListener("input", async () => {
//         const query = searchInput.value.trim();
//         if (query.length === 0) {
//             suggestionsList.innerHTML = "";
//             suggestionsList.style.display = "none";
//             return;
//         }

//         const suggestions = await fetchSuggestions(query);
//         renderSuggestions(suggestions);
//     });
// });


// NEW VERSION FOR ALL SIMPLE SEARCH ENGINE ROUTES
async function setupAutocomplete(inputId, suggestionsContainerId, endpoint) {
    const input = document.getElementById(inputId);
    const suggestionsContainer = document.getElementById(suggestionsContainerId);

    if (!input || !suggestionsContainer) {
        console.error(`Invalid input or suggestions container: ${inputId}, ${suggestionsContainerId}`);
        return;
    }

    input.addEventListener('input', async () => {
        const query = input.value.trim();

        // Clear suggestions if input is empty
        if (!query) {
            suggestionsContainer.innerHTML = '';
            return;
        }

        try {
            const response = await fetch(`${endpoint}?query=${query}`);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const suggestions = await response.json();

            // Clear previous suggestions
            suggestionsContainer.innerHTML = '';

            // If no suggestions, exit early
            if (!suggestions.length) {
                return;
            }

            // Populate suggestions
            suggestions.forEach(suggestion => {
                const suggestionItem = document.createElement('div');
                suggestionItem.textContent = suggestion;
                suggestionItem.classList.add('suggestion-item');

                // Handle click on suggestion
                suggestionItem.addEventListener('click', () => {
                    input.value = suggestion;
                    suggestionsContainer.innerHTML = '';
                });

                suggestionsContainer.appendChild(suggestionItem);
            });
        } catch (error) {
            console.error(`Error fetching suggestions from ${endpoint}:`, error);
        }
    });

    // Clear suggestions on blur
    input.addEventListener('blur', () => {
        setTimeout(() => (suggestionsContainer.innerHTML = ''), 100);
    });
}

// Apply autocomplete to both inputs
setupAutocomplete('search_category', 'suggestions-category', '/categories/autocomplete');
setupAutocomplete('search_disorder', 'suggestions-disorder', '/disorders/autocomplete');

