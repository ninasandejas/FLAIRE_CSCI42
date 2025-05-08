document.addEventListener("DOMContentLoaded", () => {
  const outfitTab = document.getElementById("explore-outfits-tab");
  const showroomTab = document.getElementById("explore-showrooms-tab");
  const grid = document.getElementById("explore-grid");

  const loadOutfits = () => {
    fetch("/social/explore-outfits/")
      .then(response => response.json())
      .then(data => {
        grid.innerHTML = "";
        data.images.forEach(image => {
          const img = document.createElement("img");
          img.src = image.url;
          img.classList.add("grid-image");
          img.dataset.outfitId = image.id;
          grid.appendChild(img);
        });
      });
  };

  const loadShowrooms = () => {
    fetch("/social/explore-showrooms/")
      .then(response => response.json())
      .then(data => {
        grid.innerHTML = "";
        data.showrooms.forEach(showroom => {
          const div = document.createElement("div");
          div.classList.add("showroom-card");
          div.innerHTML = `
            <img src="${showroom.url}" class="grid-image" />
            <p>${showroom.title}</p>
          `;
          grid.appendChild(div);
        });
      });
  };

  outfitTab.addEventListener("click", loadOutfits);
  showroomTab.addEventListener("click", loadShowrooms);

  loadOutfits();
});
