let currentPage = 1;
const resultsPerPage = 10;
let totalPages = 1;

function searchBooks(page = 1) {
    currentPage = page;
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
    .then(async data => {
        searchResults.innerHTML = "";

        if (!data.items) {
            searchResults.innerHTML = "<p>No books found.</p>";
            paginationContainer.style.display = "none";
            return;
        }

        const maxResults = 1000;
        const totalItems = Math.min(data.totalItems || 0, maxResults);
        totalPages = Math.ceil(totalItems / resultsPerPage);

        const borrowedTitles = await fetch('/borrowed_titles/')
            .then(res => res.json())
            .then(data => data.titles);

        data.items.forEach(book => {
            let bookInfo = book.volumeInfo;
            let title = bookInfo.title || "No title available";
            let authors = bookInfo.authors ? bookInfo.authors.join(", ") : "Unknown author";
            let thumbnail = bookInfo.imageLinks ? bookInfo.imageLinks.thumbnail : "https://books.google.com/googlebooks/images/no_cover_thumb.gif";
            let previewLink = bookInfo.previewLink || "#";
            let bookId = book.id || ""; // Gets Google Book ID

            let isAlreadyBorrowed = borrowedTitles.includes(title);

            let bookItem = document.createElement("div");
            bookItem.classList.add("book-item");

            bookItem.innerHTML = `
                <img src="${thumbnail}" alt="${title}">
                <h3>${title}</h3>
                <p>${authors}</p>
                <a href="${previewLink}" target="_blank">View More</a><br><br>
                <button class="checkout-button" onclick="checkoutBook('${escapeJS(title)}', '${escapeJS(authors)}', '${escapeJS(thumbnail)}', '${escapeJS(previewLink)}', '${escapeJS(bookId)}')" ${isAlreadyBorrowed ? "disabled" : ""}>
                    ${isAlreadyBorrowed ? "Already Borrowed" : "Checkout"}
                </button>
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
        paginationContainer.style.justifyContent = "center";
        paginationContainer.style.alignItems = "center";
        paginationContainer.style.gap = "20px";
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
    pageInfo.style.fontWeight = "bold";
    pageInfo.style.minWidth = "120px"; 

    if (currentPage > 1) {
        paginationContainer.appendChild(prevButton);
    }

    paginationContainer.appendChild(pageInfo);

    if (currentPage < totalPages) {
        paginationContainer.appendChild(nextButton);
    }
}

function toggleContactForm() {
    const form = document.getElementById("contact-form-popup");
    form.classList.toggle("contact-hidden");
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#contact-form-popup form");
    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            const data = {
                name: form.name.value,
                email: form.email.value,
                subject: form.subject.value,
                message: form.message.value
            };

            try {
                const response = await fetch("/contact/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCSRFToken()
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();   
                const formResponse = document.getElementById("form-response");
                formResponse.textContent = result.message;
                formResponse.style.color = result.status === "success" ? "green" : "red";
                formResponse.style.opacity = "1";

                setTimeout(() => {
                    formResponse.style.transition = "opacity 0.8s ease";
                    formResponse.style.opacity = "0";
                }, 3000);

                if (result.status === "success") {
                    form.reset();
                    toggleContactForm();
                }

            } catch (err) {
                alert("Something went wrong. Please try again.");
                console.error(err);
            }
        });
    }

    // Click and Enter for book search triggers
    const searchInput = document.getElementById("uquery");
    const searchButton = document.getElementById("search-button");

    // Pressing Enter triggers search
    if (searchInput) {
        searchInput.addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                searchBooks(1);
            }
        });
    }

    // Clicking the Search button triggers search
    if (searchButton) {
        searchButton.addEventListener("click", function() {
            searchBooks(1);
        });
    }
});

function getCSRFToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
            return decodeURIComponent(cookie.split("=")[1]);
        }
    }
    return "";
}

function checkoutBook(title, authors, thumbnail, previewLink, bookId) {
    fetch("/checkout/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({
            title: title,
            author: authors,
            genre: "Unknown",
            quantity: 1,
            thumbnail: thumbnail,
            preview_link: previewLink,
            book_id: bookId
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        searchBooks(currentPage);  // Refresh after checkout
    })
    .catch(error => {
        console.error("Error checking out book:", error);
        alert("Failed to checkout book.");
    });
}

function escapeJS(str) {
    return str.replace(/'/g, "\\'").replace(/"/g, '\\"');
}