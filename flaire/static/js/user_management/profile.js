document.addEventListener('DOMContentLoaded', () => {
    const wishlistItems = JSON.parse(document.getElementById('wishlist-data').textContent);

    const wishlistImage = document.getElementById('wishlist-main-image');
    const prevButton = document.querySelector('.wishlist-nav-prev');
    const nextButton = document.querySelector('.wishlist-nav-next');

    let currentIndex = 0;

    const updateWishlistImage = () => {
        if (wishlistItems.length > 0) {
            wishlistImage.src = wishlistItems[currentIndex].image;
            wishlistImage.alt = wishlistItems[currentIndex].name;
        }
    };

    prevButton.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + wishlistItems.length) % wishlistItems.length;
        updateWishlistImage();
    });

    nextButton.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % wishlistItems.length;
        updateWishlistImage();
    });

    updateWishlistImage();
}); document.addEventListener("DOMContentLoaded", function () {
    const gridContainer = document.getElementById("posts-grid-container");
    const modal = document.getElementById("outfit-modal");
    const closeBtn = document.querySelector(".close-btn");
    const commentForm = document.getElementById("comment-form");
    const commentInput = document.getElementById("comment-input");
    const commentsSection = document.getElementById("modal-comments");
    const commentsList = document.getElementById("modal-comments-list");
    const listItemsSection = document.getElementById("modal-listed-items");
    const tabButtons = document.querySelectorAll(".mini-tab");
    const modalOverlay = document.getElementById("modal-overlay");

    loadOutfits();
    function loadOutfits() {
        const loggedInProfile = document.querySelector('meta[name="logged-in-profile"]').content;
        const profileCurrentlyViewing = document.querySelector('meta[name="profile-currently-viewing"]').content;

        const endpoint = loggedInProfile === profileCurrentlyViewing
            ? "/outfit-grid-images/"
            : `/outfit-grid-images/${profileCurrentlyViewing}/`;

        fetch(endpoint)
            .then(res => res.json())
            .then(data => {
                data.images.forEach(outfit => {
                    const img = document.createElement("img");
                    img.src = outfit.url;
                    img.alt = `Outfit ${outfit.id}`;
                    img.classList.add("outfit-image");
                    img.dataset.outfitId = outfit.id;

                    const wrapper = document.createElement("div");
                    wrapper.classList.add("post-wrapper");
                    wrapper.appendChild(img);
                    gridContainer.append(wrapper);
                });
            })
            .catch(err => console.error("Error loading outfits:", err));
    }

    gridContainer.addEventListener("click", e => {
        const clicked = e.target.closest(".outfit-image");
        if (!clicked) return;

        const outfitId = clicked.dataset.outfitId;
        fetch(`/outfit-details/${outfitId}/`)
            .then(res => res.json())
            .then(data => showOutfitPostModal(data));
    });

    function showOutfitPostModal(data) {
        modalOverlay.style.display = "block";
        modal.classList.remove("hidden");
        document.getElementById("modal-image").src = data.url;
        document.getElementById("modal-caption").textContent = data.caption;
        document.getElementById("modal-owner").textContent = "@" + data.owner;
        document.getElementById("modal-tags").textContent = data.tags.map(t => `#${t}`).join(" ");
        modal.dataset.outfitId = data.id;

        // 🧥 Listed Items Section
        listItemsSection.innerHTML = "";
        if (data.listed_items.length) {
            data.listed_items.forEach(item => {
                const div = document.createElement("div");
                div.classList.add("listed-item");
                div.dataset.itemId = item.id;

                const isInCloset = item.is_in_closet;
                div.innerHTML = `
                    <img src="${item.url}" />
                    <div class="listed-item-details">
                      <div><strong>${item.name}</strong></div>
                      <div>${item.brand}</div>
                      <div style="font-size: 0.7rem; color: #7B6A73;">uploaded by @${item.owner}</div>
                      <div class="hover-buttons">
                        <button class="closet-btn" ${isInCloset ? 'disabled' : ''}>
                            ${isInCloset ? "Already in Closet" : "Add to Closet"}
                        </button>
                        <button class="wishlist-btn">Add to Wishlist</button>
                      </div>
                    </div>
                `;
                listItemsSection.appendChild(div);

                if (!isInCloset) {
                    const closetBtn = div.querySelector(".closet-btn");
                    closetBtn.addEventListener("click", () => {
                        fetch(`/add-to-closet/${item.id}/`, {
                            method: "POST",
                            headers: {
                                "X-CSRFToken": getCSRFToken(),
                            },
                        })
                            .then(res => res.json())
                            .then(data => {
                                if (data.status === "added") {
                                    closetBtn.textContent = "Added to Closet";
                                    closetBtn.disabled = true; // Disable the button after adding
                                } else if (data.status === "already_in_closet") {
                                    closetBtn.textContent = "Already in Closet";
                                    closetBtn.disabled = true;
                                } else {
                                    alert(data.message || "An error occurred.");
                                }
                            })
                            .catch(err => {
                                console.error("Error adding to closet:", err);
                                alert("Something went wrong. Please try again.");
                            });
                    });
                }

                // Add to Wishlist Button Logic
                const wishlistBtn = div.querySelector(".wishlist-btn");
                wishlistBtn.addEventListener("click", () => {
                    fetch(`/toggle-wishlist/${item.id}/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": getCSRFToken(),
                        },
                    })
                        .then(res => res.json())
                        .then(resp => {
                            wishlistBtn.textContent = resp.status === "added"
                                ? "Remove from Wishlist"
                                : "Add to Wishlist";
                        })
                        .catch(err => {
                            console.error("Wishlist toggle error:", err);
                            alert("Something went wrong while updating your wishlist.");
                        });
                });
            });
        } else {
            listItemsSection.innerHTML = "<p>No items listed.</p>";
        }

        //  Comments Section
        commentsList.innerHTML = "";
        if (data.comments.length) {
            data.comments.forEach(c => {
                const div = document.createElement("div");
                div.classList.add("comment");
                div.innerHTML = `<strong>@${c.author}</strong> ${c.entry}`;
                commentsList.appendChild(div);
            });
        } else {
            commentsList.innerHTML = "<p>No comments yet.</p>";
        }

        //  Tab Logic
        tabButtons.forEach(t => t.classList.remove("active"));
        commentsSection.classList.add("hidden");
        listItemsSection.classList.add("hidden");

        const defaultTab = tabButtons[0];
        defaultTab.classList.add("active");

        if (defaultTab.dataset.tab === "comments") {
            commentsSection.classList.remove("hidden");
        } else if (defaultTab.dataset.tab === "list") {
            listItemsSection.classList.remove("hidden");
        }

        //  Like (Heart) Button Logic
        const heartButton = document.getElementById("like-button");
        if (heartButton) {
            const heartIcon = heartButton.querySelector("img");

            // Set heart icon based on is_liked from backend
            heartIcon.src = data.is_liked
                ? "/static/img/liked.png"
                : "/static/img/unliked.png";

            heartButton.replaceWith(heartButton.cloneNode(true)); // Remove old event listeners
            const newHeartButton = document.getElementById("like-button");
            newHeartButton.addEventListener("click", () => {
                fetch(`/toggle-like-outfit/${data.id}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                    },
                })
                    .then(res => res.json())
                    .then(resp => {
                        heartIcon.src = resp.status === "liked"
                            ? "/static/img/liked.png"
                            : "/static/img/unliked.png";
                    })
                    .catch(err => {
                        console.error("Like button error:", err);
                        alert("Couldn't update your like. Try again?");
                    });
            });
        }

        modal.classList.remove("hidden");
    }



    tabButtons.forEach(tab => {
        tab.addEventListener("click", () => {
            tabButtons.forEach(t => t.classList.remove("active"));
            commentsSection.classList.add("hidden");
            listItemsSection.classList.add("hidden");

            tab.classList.add("active");
            if (tab.dataset.tab === "likes") {
                tabContent.innerHTML = `<p>${data.likes} like${data.likes !== 1 ? "s" : ""}</p>`;
            }
            else if (tab.dataset.tab === "comments") {
                commentsSection.classList.remove("hidden");
            } else if (tab.dataset.tab === "list") {
                listItemsSection.classList.remove("hidden");
            }

        });
    });

    // close modal
    closeBtn.addEventListener("click", () => {
        modal.classList.add("hidden");
        modalOverlay.style.display = "none";
    });

    // submit new comment
    if (commentForm) {
        commentForm.addEventListener("submit", e => {
            e.preventDefault();
            const text = commentInput.value.trim();
            if (!text) return;

            const id = modal.dataset.outfitId;
            fetch(`/submit-comment/${id}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify({ entry: text }),
            })
                .then(res => {
                    if (!res.ok) throw new Error("Network error");
                    return res.json();
                })
                .then(newC => {
                    // prepend the new comment
                    const div = document.createElement("div");
                    div.classList.add("comment");
                    div.innerHTML = `<strong>@${newC.author}</strong> ${newC.entry}`;
                    const wishlistBtn = div.querySelector(".wishlist-btn");
                    wishlistBtn.dataset.itemId = item.id;
                    wishlistBtn.addEventListener("click", () => {
                        fetch(`/toggle-wishlist/${item.id}/`, {
                            method: "POST",
                            headers: {
                                "X-CSRFToken": getCSRFToken(),
                            },
                        })
                            .then(res => res.json())
                            .then(data => {
                                wishlistBtn.textContent = data.status === "added" ? "Remove from Wishlist" : "Add to Wishlist";
                            });
                    });



                    commentsList.prepend(div);
                    commentInput.value = "";
                })
                .catch(err => {
                    console.error("Error posting comment:", err);
                    alert("Could not post comment.");
                });
        });
    }

    function getCSRFToken() {
        return (
            document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
            document.cookie
                .split("; ")
                .find(row => row.startsWith("csrftoken"))
                ?.split("=")[1] || ""
        );
    }



});

