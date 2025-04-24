document.addEventListener("DOMContentLoaded", function () {
    const gridContainer = document.getElementById("posts-grid-container");

    loadOutfits();

    function loadOutfits() {

        fetch(`/outfit-grid-images/`)
            .then((response) => response.json())
            .then((data) => {
                data.images.forEach(outfit => {
                    const img = document.createElement("img");
                    img.src = outfit.url;
                    img.alt = `Outfit ${outfit.id}`;
                    img.classList.add("outfit-image");

                    const wrapper = document.createElement("div");
                    wrapper.classList.add("post-wrapper");
                    wrapper.appendChild(img);
                    gridContainer.appendChild(wrapper);
                });
            })

            .catch(error => {
                console.error("Error loading outfits:", error);
            });

    }

});