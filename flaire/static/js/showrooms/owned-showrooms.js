let currentPage = 1;
let showroomId = null;

function loadShowrooms(page = 1) {
  currentPage = page;

  fetch(`/showrooms/owned/?page=${page}`)
    .then(res => res.json())
    .then(data => {
      const grid = document.getElementById('showroom-grid');
      grid.innerHTML = '';

      // previous arrow
      const prevArrow = document.createElement('div');
      prevArrow.className = 'thumbnail pagination-arrow';
      prevArrow.innerHTML = `
        <button id="prev-btn" class="arrow-button" ${page === 1 ? 'disabled' : ''}>
          &#8592;
        </button>
      `;
      grid.appendChild(prevArrow);

      // add div button for create showrooms
      if (page === 1) {
        const container = document.createElement('div');
        container.className = 'thumbnail-container';
      
        const addDiv = document.createElement('div');
        addDiv.className = 'thumbnail add';
        addDiv.innerHTML = `<div class="plus">+</div>`;
        addDiv.addEventListener('click', () => {
          window.location.href = '/showrooms/create/';
        });
      
        const label = document.createElement('p');
        label.className = 'add-label';
        label.textContent = 'Create showroom';
      
        container.appendChild(addDiv);
        container.appendChild(label);
        grid.appendChild(container);
      }

      // each showroom (shown through cover image: thumbnails)
      data.showrooms.forEach(showroom => {
        const thumb = document.createElement('div');
        thumb.className = 'thumbnail';
        thumb.innerHTML = `
          <a href = "/showrooms/${showroom.slug}-${showroom.id}/">
            <img src="${showroom.cover_image}" alt="${showroom.title}" />
          </a>
          <p>${showroom.title}</p>
        `;
        grid.appendChild(thumb);
      });

      // next arrow
      const nextArrow = document.createElement('div');
      nextArrow.className = 'thumbnail pagination-arrow';
      nextArrow.innerHTML = `
        <button id="next-btn" class="arrow-button" ${!data.has_next ? 'disabled' : ''}>
          &#8594;
        </button>
      `;
      grid.appendChild(nextArrow);
      
      currentPage = data.current_page;
    });
}

document.getElementById('showroom-grid').addEventListener('click', function (e) {
  const target = e.target;

  if (target.id === 'prev-btn' && !target.disabled) {
    if (currentPage > 1) loadShowrooms(currentPage - 1);
  }

  if (target.id === 'next-btn' && !target.disabled) {
    loadShowrooms(currentPage + 1);
  }
});

loadShowrooms();