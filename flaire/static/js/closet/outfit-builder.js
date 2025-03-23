document.addEventListener("DOMContentLoaded", function () {
    const gridContainer = document.getElementById("grid-container");
    const dropzone = document.getElementById("collage-dropzone");
    const saveButton = document.getElementById("save-button");
    const totalSquares = 15;
    let selectedElement = null;

    loadClothingImages();

    setupDropzoneEvents();
    setupKeyboardEvents();

    function loadClothingImages() {
        fetch("/closet/images/")
            .then((response) => response.json())
            .then((data) => {
                const images = data.images;

                for (let i = 0; i < totalSquares; i++) {
                    const square = document.createElement("div");
                    square.classList.add("grid-item");

                    if (i === 0) {
                        const plusLink = document.createElement("a");
                        plusLink.href = "/closet/add/";
                        plusLink.classList.add("add-item-link");
                        plusLink.innerHTML = "+";
                        square.appendChild(plusLink);
                    } else if (images[i - 1]) {
                        const img = document.createElement("img");
                        img.src = images[i - 1];
                        img.alt = `Clothing Item ${i}`;
                        img.draggable = true;
                        img.classList.add("draggable-item");
                        Object.assign(img.style, {
                            width: "100%",
                            height: "100%",
                            objectFit: "cover"
                        });

                        img.addEventListener("dragstart", (e) => {
                            e.dataTransfer.setData("text/plain", img.src);
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

            const imageUrl = e.dataTransfer.getData("text/plain");

            const wrapper = document.createElement("div");
            wrapper.classList.add("resizable-draggable");
            Object.assign(wrapper.style, {
                position: "absolute",
                left: `${e.offsetX - 50}px`,
                top: `${e.offsetY - 50}px`,
                width: "100px",
                height: "100px"
            });

            const img = document.createElement("img");
            img.src = imageUrl;
            Object.assign(img.style, {
                width: "100%",
                height: "100%",
                objectFit: "contain",
                pointerEvents: "none"
            });

            wrapper.appendChild(img);
            dropzone.appendChild(wrapper);

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
        });
    }

    function setupKeyboardEvents() {
        document.addEventListener("keydown", (e) => {
            if ((e.key === "Delete" || e.key === "Backspace") && selectedElement) {
                selectedElement.remove();
                selectedElement = null;
            }
        });
    }

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
});



