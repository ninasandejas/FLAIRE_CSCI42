document.addEventListener("DOMContentLoaded", () => {
  const outfitTab = document.getElementById("explore-outfits-tab");
  const showroomTab = document.getElementById("explore-showrooms-tab");
  const outfitsGrid = document.getElementById("outfits-grid");
  const showroomsGrid = document.getElementById("showrooms-grid");

  const activateTab = (tabToActivate) => {
    [outfitTab, showroomTab].forEach(tab => tab.classList.remove("active"));
    tabToActivate.classList.add("active");
  };

  outfitTab.addEventListener("click", () => {
    activateTab(outfitTab);
    outfitsGrid.classList.remove("hidden-grid");
    showroomsGrid.classList.add("hidden-grid");
    outfitsGrid.innerHTML = ""; // Clear previous content
    loadOutfits();
  });

  showroomTab.addEventListener("click", () => {
    activateTab(showroomTab);
    outfitsGrid.classList.add("hidden-grid");
    showroomsGrid.classList.remove("hidden-grid");
    showroomsGrid.innerHTML = ""; // Clear previous content
    loadShowrooms();
  });

  // Initial load of outfits
  loadOutfits();

  function loadOutfits() {
    fetch(`/social/explore-outfits/`)
      .then(res => res.json())
      .then(data => {
        outfitsGrid.innerHTML = ""; // Clear previous content
        data.images.forEach(outfit => {
          const img = document.createElement("img");
          img.src = outfit.url;
          img.alt = `Outfit ${outfit.id}`;
          img.classList.add("outfit-image");
          img.dataset.outfitId = outfit.id;

          const wrapper = document.createElement("div");
          wrapper.classList.add("post-wrapper");
          wrapper.appendChild(img);
          outfitsGrid.appendChild(wrapper);
        });

        // Attach click handler for each outfit
        outfitsGrid.querySelectorAll(".outfit-image").forEach(img => {
          img.addEventListener("click", (e) => {
            const outfitId = e.currentTarget.dataset.outfitId;
            fetch(`/closet/${outfitId}/`)
              .then(res => res.json())
              .then(data => showOutfitPostModal(data));
          });
        });
      })
      .catch(err => console.error("Error loading outfits:", err));
  }

  function loadShowrooms() {
    console.log('Loading showrooms...');  // Debugging log

    fetch(`/explore-showrooms/`)
      .then(res => res.json())
      .then(data => {
        console.log('Showrooms data:', data);  // Log the data to ensure it's correct
        showroomsGrid.innerHTML = ""; // Clear previous content
        data.showrooms.forEach(showroom => {
          const img = document.createElement("img");
          img.src = showroom.url; // Assuming this is the cover_image URL
          img.alt = showroom.title;
          img.classList.add("showroom-thumbnail");
          img.dataset.showroomId = showroom.id; // Store showroom ID

          const wrapper = document.createElement("div");
          wrapper.classList.add("post-wrapper");
          wrapper.appendChild(img);
          showroomsGrid.appendChild(wrapper);
        });

        // Attach click handler for each showroom
        showroomsGrid.querySelectorAll(".showroom-thumbnail").forEach(img => {
          img.addEventListener("click", (e) => {
            const showroomId = e.currentTarget.dataset.showroomId;
            window.location.href = `/showroom/${showroomId}/`; // Redirect to showroom details page
          });
        });
      })
      .catch(err => console.error("Error loading showrooms:", err));
  }

  
});
