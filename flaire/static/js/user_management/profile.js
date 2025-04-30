document.addEventListener("DOMContentLoaded", function () {
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
        fetch(`/outfit-grid-images/`)
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
        // store outfit ID for comment form
        modal.dataset.outfitId = data.id;

        listItemsSection.innerHTML = "";
        if (data.listed_items.length) {
            data.listed_items.forEach(item => {
                const div = document.createElement("div");
                div.classList.add("listed-item");
                div.innerHTML = `
            <img src="${item.url}" />
            <div class="listed-item-details">
              <div><strong>${item.name}</strong></div>
              <div>${item.brand}</div>
              <div style= "font-size: 0.7rem; color: #7B6A73;">uploaded by @${item.owner}</div>
              <div class="hover-buttons">
              <button class="closet-btn">Add to Closet</button>
              <button class="wishlist-btn">Add to Wishlist</button>
              </div>
            </div>
          `;
                listItemsSection.appendChild(div);
            });
        } else {
            listItemsSection.innerHTML = "<p>No items listed.</p>";
        }

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

        tabButtons.forEach(t => t.classList.remove("active"));
        commentsSection.classList.add("hidden");
        listItemsSection.classList.add("hidden");


        const defaultTab = tabButtons[0];
        defaultTab.classList.add("active");
        // will add likes in a sec
        if (defaultTab.dataset.tab === "comments") {
            commentsSection.classList.remove("hidden");
        } else if (defaultTab.dataset.tab === "list") {
            listItemsSection.classList.remove("hidden");
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
            document.querySelector('meta[name="csrf-token"]')?.content ||
            ""
        );
    }
});