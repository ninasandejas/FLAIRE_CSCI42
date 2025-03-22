document.addEventListener("DOMContentLoaded", function () {
    const gridContainer = document.getElementById("grid-container");
    const totalSquares = 15; // Set your desired fixed number of grid squares

    fetch("/closet/images/")
        .then((response) => response.json())
        .then((data) => {
            const images = data.images;

            for (let i = 0; i < totalSquares; i++) {
                const square = document.createElement("div");
                square.classList.add("grid-item");

                if (i === 0) {
                    // First square = "+" button
                    const plusLink = document.createElement("a");
                    plusLink.href = "/closet/add/"; // change this to your clothing item add view url
                    plusLink.classList.add("add-item-link");
                    plusLink.innerHTML = "+";
                    square.appendChild(plusLink);
                } else if (images[i - 1]) {
                    // Populate with clothing images
                    const img = document.createElement("img");
                    img.src = images[i - 1];
                    img.alt = `Clothing Item ${i}`;
                    img.style.width = "100%";
                    img.style.height = "100%";
                    img.style.objectFit = "cover";
                    square.appendChild(img);
                }

                gridContainer.appendChild(square);
            }
        })
        .catch((error) => {
            console.error("Error loading images:", error);
        });
});