let currentPage = 1;
const resultsPerPage = 10; 
let totalPages = 1; 

function searchBooks(page = 1) {
    let query = document.getElementById("uquery").value.trim();
    let filter = document.getElementById("filterDropdown").value;
    let searchResults = document.getElementById("search-results");
    const paginationContainer = document.getElementById("pagination");

    if (!query) {
        searchResults.innerHTML = "<p>Please enter a search query.</p>";
        paginationContainer.style.display = "none";
        return;
    }

    let apiUrl = "https://www.googleapis.com/books/v1/volumes?q=";
    if (filter === "title") {
        apiUrl += `intitle:${query}`;
    } else if (filter === "author") {
        apiUrl += `inauthor:${query}`;
    } else {
        apiUrl += query;
    }

    fetch(`${apiUrl}&startIndex=${(page - 1) * resultsPerPage}&maxResults=${resultsPerPage}`)
        .then(response => response.json())
        .then(data => {
            searchResults.innerHTML = "";

            if (!data.items) {
                searchResults.innerHTML = "<p>No books found.</p>";
                paginationContainer.style.display = "none";
                return;
            }

            totalPages = data.totalItems ? Math.ceil(data.totalItems / resultsPerPage) : 1;

            data.items.forEach(book => {
                let bookInfo = book.volumeInfo;
                let title = bookInfo.title || "No title available";
                let authors = bookInfo.authors ? bookInfo.authors.join(", ") : "Unknown author";
                let thumbnail = bookInfo.imageLinks ? bookInfo.imageLinks.thumbnail : "https://via.placeholder.com/150";
                let previewLink = bookInfo.previewLink || "#";

                let bookItem = document.createElement("div");
                bookItem.classList.add("book-item");

                bookItem.innerHTML = `
                    <img src="${thumbnail}" alt="${title}">
                    <h3>${title}</h3>
                    <p>${authors}</p>
                    <a href="${previewLink}" target="_blank">View More</a>
                `;

                searchResults.appendChild(bookItem);
            });

            updatePaginationButtons();
        })
        .catch(error => {
            console.error("Error fetching data:", error);
            searchResults.innerHTML = "<p>Something went wrong. Please try again.</p>";
        });
}

function updatePaginationButtons() {
    const paginationContainer = document.getElementById("pagination");
    paginationContainer.innerHTML = "";

    if (totalPages <= 1) {
        paginationContainer.style.display = "none";
        return;
    } else {
        paginationContainer.style.display = "flex";
    }

    const prevButton = document.createElement("button");
    prevButton.textContent = "Previous";
    prevButton.disabled = currentPage === 1;
    prevButton.onclick = () => {
        if (currentPage > 1) {
            currentPage--;
            searchBooks(currentPage);
        }
    };

    const nextButton = document.createElement("button");
    nextButton.textContent = "Next";
    nextButton.disabled = currentPage >= totalPages;
    nextButton.onclick = () => {
        if (currentPage < totalPages) {
            currentPage++;
            searchBooks(currentPage);
        }
    };

    const pageInfo = document.createElement("span");
    pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;

    paginationContainer.appendChild(prevButton);
    paginationContainer.appendChild(pageInfo);
    paginationContainer.appendChild(nextButton);
}

// Allow pressing "Enter" to trigger search
document.getElementById("uquery").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        searchBooks(1);
    }
});