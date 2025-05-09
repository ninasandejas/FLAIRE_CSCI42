document.addEventListener("DOMContentLoaded", () => {
  const outfitTab = document.getElementById("following-outfits-tab");
  const showroomTab = document.getElementById("following-showrooms-tab");
  const outfitsGrid = document.getElementById("outfits-grid");
  const showroomsGrid = document.getElementById("showrooms-grid");

  const activateTab = (tabToActivate) => {
    [outfitTab, showroomTab].forEach(tab => tab.classList.remove("active"));
    tabToActivate.classList.add("active");
  };

  outfitTab.addEventListener("click", () => {
    activateTab(outfitTab);
    outfitsGrid.classList.remove("hidden-grid");
    showroomsGrid.innerHTML = ""; 
    showroomsGrid.classList.add("hidden-grid");
    outfitsGrid.innerHTML = "";
    loadOutfits();
  });

  showroomTab.addEventListener("click", () => {
    activateTab(showroomTab);
    outfitsGrid.classList.add("hidden-grid");
    outfitsGrid.innerHTML = ""; 
    showroomsGrid.classList.remove("hidden-grid");
    showroomsGrid.innerHTML = "";
    loadShowrooms();
  });

  loadOutfits();

  function loadOutfits() {
    fetch(`/social/following-outfits/`)
      .then(res => res.json())
      .then(data => {
        outfitsGrid.innerHTML = "";
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

        outfitsGrid.querySelectorAll(".outfit-image").forEach(img => {
          img.addEventListener("click", (e) => {
            const outfitId = e.currentTarget.dataset.outfitId;
            fetch(`/closet/${outfitId}/`)
              .then(res => res.json())
              .then(data => showOutfitPostModal(data));
          });
        });
      })
      .catch(err => console.error("Error loading following outfits:", err));
  }

  function loadShowrooms() {
    fetch(`/social/following-showrooms/`)
      .then(res => res.json())
      .then(data => {
        showroomsGrid.innerHTML = "";
        data.images.forEach(showroom => {
          const img = document.createElement("img");
          img.src = showroom.cover_image;  
          img.alt = showroom.title;
          img.classList.add("showroom-image");
          img.dataset.showroomId = showroom.id;

          const wrapper = document.createElement("div");
          wrapper.classList.add("post-wrapper");
          wrapper.appendChild(img);
          showroomsGrid.appendChild(wrapper);
  
          img.addEventListener("click", () => {
            window.location.href = `/showrooms/${showroom.slug}-${showroom.id}/`;
          });
        });
      })
      .catch(error => console.error('Error loading showrooms:', error));
  }
});
