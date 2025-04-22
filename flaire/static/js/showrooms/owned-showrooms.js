// document.addEventListener("DOMContentLoaded", function () {
//     const showroomsList = document.getElementById("showrooms-list");

//     fetch('/showrooms/get-showrooms')



// });

let currentPage = 1;

function loadShowrooms(page = 1) {
  fetch(`/showrooms/owned/?page=${page}`)
    .then(res => res.json())
    .then(data => {
      const grid = document.getElementById('showroom-grid');
      grid.innerHTML = '';

      // add button
      if (page === 1) {
        const addDiv = document.createElement('div');
        addDiv.className = 'thumbnail add';
        addDiv.innerHTML = `<a href="/showrooms/create"><div class="plus">+</div></a>`;
        grid.appendChild(addDiv);
      }

      // showroom thumbnails
      data.showrooms.forEach(showroom => {
        const thumb = document.createElement('div');
        thumb.className = 'thumbnail';
        thumb.innerHTML = `
          <img src="${showroom.cover_image}" alt="${showroom.title}" />
          <p>${showroom.title}</p>
        `;
        grid.appendChild(thumb);
      });

      // updating button states
      document.getElementById('prev-btn').disabled = !data.has_previous;
      document.getElementById('next-btn').disabled = !data.has_next;
      currentPage = data.current_page;
    });
}

document.getElementById('prev-btn').addEventListener('click', () => {
  if (currentPage > 1) loadShowrooms(currentPage - 1);
});
document.getElementById('next-btn').addEventListener('click', () => {
  loadShowrooms(currentPage + 1);
});

loadShowrooms();
