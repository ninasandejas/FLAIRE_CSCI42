let currentPage = 1;
let showroomId = null;


// loading of list of all showrooms the user has access to
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

      // add button
      // if (page === 1) {
      //   const addDiv = document.createElement('div');
      //   addDiv.className = 'thumbnail add';
      //   addDiv.innerHTML = `<div class="plus">+</div>`;
      //   addDiv.addEventListener('click', () => {
      //     const dialog = document.getElementById('dialog');
      
      //     // Temporary listener: wait until HTMX finishes swapping content into #dialog
      //     const handleSwap = function (e) {
      //       if (e.target === dialog) {    
      //         // Show modal
      //         const modal = new bootstrap.Modal(document.getElementById('create-modal'));
      //         modal.show();
      
      //         // Remove listener after it's done to prevent re-triggers
      //         document.body.removeEventListener('htmx:afterSwap', handleSwap);
      //       }
      //     };
      
      //     document.body.addEventListener('htmx:afterSwap', handleSwap);
      
      //     // Make the HTMX request
      //     htmx.ajax('GET', '/showrooms/create/', {
      //       target: dialog,
      //       swap: 'innerHTML',
      //       headers: {
      //         'HX-Request': 'true'
      //       }
      //     });
      //   });
      //   grid.appendChild(addDiv);
      // }
      if (page === 1) {
        const addDiv = document.createElement('div');
        addDiv.className = 'thumbnail add';
        addDiv.innerHTML = `<div class="plus">+</div>`;
        addDiv.addEventListener('click', () => {
          window.location.href = '/showrooms/create/';
          // currentStep = 1;
          // nextStep(1);
          // document.getElementById("create-modal").style.display = "flex";
        });
        grid.appendChild(addDiv);
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

// function showModal(){
//   document.getElementById("create-modal").removeAttribute("hidden");
    
//     // Wait for modal to be visible before initializing select2
//     $('.select2').select2({
//       placeholder: "Search and select collaborators",
//       width: '100%',
//       dropdownParent: $('#create-modal')  // important inside modals
//     });
// }

loadShowrooms();

// document.body.addEventListener('htmx:afterSwap', function(evt) {
//   if (evt.target.id === 'dialog') {
//     $('.select2').select2({
//       placeholder: "Search and select collaborators",
//       width: '100%',
//       dropdownParent: $('#create-modal') // ensures it renders properly in modals
//     });
//   }
// });