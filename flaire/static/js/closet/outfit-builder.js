//itemID = UI-only ID to track items as visual assets
//clothingItemId = real database clothingItem ID for outfit_items

document.addEventListener("DOMContentLoaded", function () {
    const gridContainer = document.getElementById("grid-container");
    const dropzone = document.getElementById("collage-dropzone");
    const saveButton = document.getElementById("save-button");
    const totalSquares = 15;
    const outfitItems = new Set();  //sets prevent duplicates
    let selectedElement = null;

    loadClothingImages("TOP"); //default drawer or category

    setupDropzoneEvents();
    setupKeyboardEvents();

    const tabs = document.querySelectorAll(".drawer-tab");

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");

            const category = tab.dataset.category;
            loadClothingImages(category);
        });
    });

    function loadClothingImages(category = "TOP") {
        gridContainer.innerHTML = ""; // clear the grid

        fetch(`/closet/images/?category=${category}`)
            .then((response) => response.json())
            .then((data) => {
                const images = data.images;

                for (let i = 0; i < totalSquares; i++) {
                    const square = document.createElement("div");
                    square.classList.add("grid-item");

                    if (i === 0) {
                        const plusLink = document.createElement("a");
                        plusLink.href = `/closet/add-clothing-item/?category=${category}`;
                        plusLink.classList.add("add-item-link");
                        plusLink.innerHTML = "+";
                        square.appendChild(plusLink);
                    } else if (images[i - 1]) {
                        const img = document.createElement("img");
                        img.src = images[i - 1].url;
                        img.dataset.clothingItemId = images[i - 1].id;
                        img.alt = `Clothing Item ${i}`;
                        img.draggable = true;
                        img.classList.add("draggable-item");

                        Object.assign(img.style, {
                            width: "auto",
                            height: "auto",
                            maxWidth: "100%",
                            maxHeight: "100%",
                            objectFit: "contain"
                        });

                        img.addEventListener("dragstart", (e) => {
                            e.dataTransfer.setData("text/plain", JSON.stringify({
                                src: img.src,
                                clothingItemId: img.dataset.clothingItemId
                            }));
                        });

                        img.addEventListener("click", () => {
                            addToDropzone(img.src, img.dataset.clothingItemId, 130, 190);
                        });

                        square.appendChild(img);
                    }

                    gridContainer.appendChild(square);
                }
            });
    }

    function setupDropzoneEvents() {
        dropzone.addEventListener("dragover", (e) => {
            e.preventDefault();
            dropzone.classList.add("drag-over");
        });

        dropzone.addEventListener("dragleave", () => {
            dropzone.classList.remove("drag-over");
        });

        dropzone.addEventListener("drop", (e) => {
            e.preventDefault();
            dropzone.classList.remove("drag-over");

            const data = JSON.parse(e.dataTransfer.getData("text/plain"));
            const x = e.offsetX;
            const y = e.offsetY;
            addToDropzone(data.src, data.clothingItemId, x, y);
        });

    }

    function addToDropzone(imageUrl, clothingItemId = null, x, y) {
        if (outfitItems.has(clothingItemId)) return;

        outfitItems.add(clothingItemId);
        const wrapper = document.createElement("div");
        wrapper.classList.add("resizable-draggable");
        wrapper.dataset.clothingItemId = clothingItemId;
        Object.assign(wrapper.style, {
            position: "absolute",
            left: `${x - 50}px`,
            top: `${y - 50}px`,
            width: "100px",
            height: "100px"
        });

        const img = document.createElement("img");
        img.src = imageUrl;
        Object.assign(img.style, {
            width: "auto",
            height: "auto",
            maxWidth: "100%",
            maxHeight: "100%",
            objectFit: "contain"
        });

        document.querySelectorAll(".resizable-draggable").forEach(el => {
            el.classList.remove("selected");
            removeResizeHandles(el);
        });

        wrapper.appendChild(img);
        dropzone.appendChild(wrapper);

        wrapper.classList.add("selected");
        addResizeHandles(wrapper);
        selectedElement = wrapper;

        const itemId = `item-${Date.now()}`; // unique ID for tracking
        wrapper.dataset.itemId = itemId;
        wrapper.style.zIndex = dropzone.children.length + 1;

        // create a thumbnail for the layering panel
        const thumbnail = document.createElement("div");
        thumbnail.classList.add("layer-thumbnail");
        thumbnail.dataset.itemId = itemId;

        const thumbImg = document.createElement("img");
        thumbImg.src = imageUrl;
        thumbnail.appendChild(thumbImg);

        const layeringPanel = document.getElementById("layer-thumbnails-area");
        layeringPanel.insertBefore(thumbnail, layeringPanel.firstChild);

        initInteract(wrapper);

        wrapper.addEventListener("click", () => {
            document.querySelectorAll(".resizable-draggable").forEach(el => {
                el.classList.remove("selected");
                removeResizeHandles(el);
            });

            wrapper.classList.add("selected");
            addResizeHandles(wrapper);
            selectedElement = wrapper;
        });
    }

    document.addEventListener("click", (e) => {
        if (e.target.classList.contains("resize-handle")) {
            return;
        }
        if (!e.target.closest(".resizable-draggable")) {
            if (selectedElement) {
                selectedElement.classList.remove("selected");
                removeResizeHandles(selectedElement);
                selectedElement = null;
            }
        }
    });

    Sortable.create(document.getElementById("layer-thumbnails-area"), {
        animation: 150,
        onSort: function () {
            // loop through layer thumbnails top-to-bottom
            const layers = document.querySelectorAll("#layering-panel .layer-thumbnail");
            layers.forEach((layer, index) => {
                const itemId = layer.dataset.itemId;
                const item = document.querySelector(`.resizable-draggable[data-item-id="${itemId}"]`);
                if (item) {
                    // topmost thumbnail has highest z-index
                    item.style.zIndex = layers.length - index;
                }
            });
        }
    });

    function setupKeyboardEvents() {
        document.addEventListener("keydown", (e) => {
            if ((e.key === "Delete" || e.key === "Backspace") && selectedElement) {
                //remove from layering panel
                const itemId = selectedElement.dataset.itemId;
                const thumbnail = document.querySelector(`#layering-panel .layer-thumbnail[data-item-id="${itemId}"]`);
                if (thumbnail) {
                    thumbnail.remove();
                }
                //remove from dropzone 
                selectedElement.remove();
                outfitItems.delete(selectedElement.dataset.clothingItemId);
                selectedElement = null;
            }
        });
    }

    const modal = document.getElementById("caption-tags-modal");
    const modalSubmitButton = document.getElementById("modal-submit");
    const captionInput = document.getElementById("caption-input");
    const tagsInput = document.getElementById("tags-input");
    const modalCloseButton = document.getElementById("modal-close");
    modalCloseButton.addEventListener("click", closeModal);

    modalCloseButton.addEventListener("click", function () {
        modal.style.display = "none";
    });

    modalSubmitButton.addEventListener("click", function () {
        const caption = captionInput.value.trim();
        const tagsRaw = tagsInput.value.trim();
        const tags = tagsRaw.split(",").map(t => t.trim()).filter(Boolean).slice(0, 3);

        const listedItemIds = Array.from(document.querySelectorAll(".resizable-draggable"))
            .map(el => el.dataset.clothingItemId)
            .filter(id => id != null);

        const dropzone = document.getElementById("collage-dropzone");

        html2canvas(dropzone, {
            backgroundColor: "#FFFFFF",
            logging: false,
        }).then(canvas => {
            canvas.toBlob(function (blob) {
                const formData = new FormData();
                // send image and listed items
                formData.append("image", blob, "outfit.png");
                formData.append("listed_item_ids", JSON.stringify(listedItemIds));

                fetch("/closet/save-outfit/", {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                    },
                })
                    .then(response => response.json())
                    .then(data => {
                        if (!data.success) {
                            throw new Error("Failed to save outfit image and listed items.");
                        }

                        const outfitId = data.outfit_id;
                        const metadataForm = new FormData();
                        // send caption and tags
                        metadataForm.append("caption", caption);
                        tags.forEach(tag => metadataForm.append("tags", tag));

                        return fetch(`/closet/save-outfit-post-metadata/${outfitId}/`, {
                            method: "POST",
                            body: metadataForm,
                            headers: {
                                "X-CSRFToken": getCSRFToken(),
                            },
                        });
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert("Outfit saved!");
                            closeModal();
                            location.reload();
                        } else {
                            throw new Error("Failed to save caption and tags.");
                        }
                    })
                    .catch(error => {
                        console.error("Error:", error);
                        alert("An error occurred while saving the outfit. Please try again.");
                    });
            }, "image/png");
        });
    });

    function initInteract(element) {
        interact(element)
            .draggable({
                listeners: {
                    move(event) {
                        const target = event.target;
                        const x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
                        const y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

                        target.style.transform = `translate(${x}px, ${y}px)`;
                        target.setAttribute('data-x', x);
                        target.setAttribute('data-y', y);
                    }
                }
            })
            .resizable({
                edges: { left: true, right: true, bottom: true, top: true },
                listeners: {
                    move(event) {
                        let x = parseFloat(event.target.getAttribute("data-x")) || 0;
                        let y = parseFloat(event.target.getAttribute("data-y")) || 0;

                        Object.assign(event.target.style, {
                            width: `${event.rect.width}px`,
                            height: `${event.rect.height}px`
                        });

                        x += event.deltaRect.left;
                        y += event.deltaRect.top;

                        event.target.style.transform = `translate(${x}px, ${y}px)`;
                        event.target.setAttribute("data-x", x);
                        event.target.setAttribute("data-y", y);
                    }
                },
                modifiers: [
                    interact.modifiers.restrictSize({
                        min: { width: 40, height: 40 },
                        max: { width: 400, height: 400 }
                    })
                ],
                inertia: true
            });
    }

    function addResizeHandles(wrapper) {
        const corners = ['nw', 'ne', 'sw', 'se'];
        for (const corner of corners) {
            const handle = document.createElement("div");
            handle.classList.add("resize-handle", corner);
            wrapper.appendChild(handle);
        }
    }

    function removeResizeHandles(wrapper) {
        wrapper.querySelectorAll(".resize-handle").forEach(handle => handle.remove());
    }

    saveButton.addEventListener("click", function () {
        document.querySelectorAll(".resizable-draggable").forEach(el => {
            el.classList.remove("selected");
            removeResizeHandles(el);
        });

        showModal();
    });

    function showModal() {
        document.getElementById("caption-tags-modal").style.display = "block";
        document.getElementById("modal-overlay").style.display = "block";
    }

    function closeModal() {
        document.getElementById("caption-tags-modal").style.display = "none";
        document.getElementById("modal-overlay").style.display = "none";
    }

    function getCSRFToken() {
        return document.cookie.split("; ").find(row => row.startsWith("csrftoken="))?.split("=")[1];
    }

});