document.addEventListener("DOMContentLoaded", () => {
  const outfitTab = document.getElementById("explore-outfits-tab");
  const showroomTab = document.getElementById("explore-showrooms-tab");
  const outfitsGrid = document.getElementById("outfits-grid");
  const showroomsGrid = document.getElementById("showrooms-grid");
  const searchInput = document.getElementById("search-bar"); 


  const activateTab = (tabToActivate) => {
    [outfitTab, showroomTab].forEach(tab => tab.classList.remove("active"));
    tabToActivate.classList.add("active");
  };

  outfitTab.addEventListener("click", () => {
    activateTab(outfitTab);
    outfitsGrid.classList.remove("hidden");
    showroomsGrid.innerHTML = ""; 
    showroomsGrid.classList.add("hidden");
    outfitsGrid.innerHTML = ""; 
    loadOutfits();
  });

  showroomTab.addEventListener("click", () => {
    activateTab(showroomTab);
    outfitsGrid.classList.add("hidden");
    outfitsGrid.innerHTML = ""; 
    showroomsGrid.classList.remove("hidden");
    showroomsGrid.innerHTML = ""; 
    loadShowrooms();
  });

  loadOutfits();

  searchInput.addEventListener("input", () => {
    const searchQuery = searchInput.value.trim().toLowerCase(); 
    if (outfitTab.classList.contains("active")) {
      loadOutfits(searchQuery); 
    } else if (showroomTab.classList.contains("active")) {
      loadShowrooms(searchQuery);
    }
  });


  function loadOutfits(searchQuery = "") {
    let url = "/social/explore-outfits/";
    if (searchQuery) {
      url += `?search=${encodeURIComponent(searchQuery)}`;
    }
  
    fetch(url)
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
      .catch(err => console.error("Error loading outfits:", err));
  }

  
  function loadShowrooms(searchQuery = "") {
    let url = "/social/explore-showrooms/";
    if (searchQuery) {
      url += `?search=${encodeURIComponent(searchQuery)}`;
    }

    fetch(url)
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
