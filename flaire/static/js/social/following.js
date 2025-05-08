document.addEventListener("DOMContentLoaded", () => {
  const outfitTab = document.getElementById("following-outfits-tab");
  const showroomTab = document.getElementById("following-showrooms-tab");
  const grid = document.getElementById("following-grid");

  const loadOutfits = () => {
    fetch("/social/following-outfits/")
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
    fetch("/social/following-showrooms/")
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
