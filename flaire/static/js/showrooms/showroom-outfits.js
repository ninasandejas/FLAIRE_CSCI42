console.log("JS file loaded");

document.addEventListener('DOMContentLoaded', () => {
  const grid = document.getElementById('outfits-grid');
  const showroomId = grid.dataset.showroomId;

  fetch(`/showrooms/${showroomId}/outfits/`)
    .then(res => res.json())
    .then(data => {
      data.outfits.forEach(outfit => {
        const img = document.createElement('img');
        img.src = outfit.image;
        img.alt = `Outfit ${outfit.id}`;

        grid.appendChild(img);
      });
    });
});