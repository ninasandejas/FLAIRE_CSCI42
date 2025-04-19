// for loading of list of showrooms
let currentPage = 1;

// for loading of create showroom and outfit-grid modal
let showroomId = null;


// loading of list of all showrooms the user has access to
function loadShowrooms(page = 1) {
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
          <a href = "/showrooms/${showroom.id}/">
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

document.getElementById('prev-btn').addEventListener('click', () => {
  if (currentPage > 1) loadShowrooms(currentPage - 1);
});
document.getElementById('next-btn').addEventListener('click', () => {
  loadShowrooms(currentPage + 1);
});

loadShowrooms();


// loading of multi-step modal
// function nextStep(step){
//   const header = document.getElementById('modal-header');
//   const modalContent = document.getElementById('modal-content');
//   const nextButton = document.getElementById('modal-next-button');

//   if(step == 1){
//     header.textContent = "Create showroom";
//     nextButton.textContent = "Next";

//     fetch('/showrooms/create-form/')
//       .then(res => res.text())
//       .then(html => {
//         modalContent.innerHTML = html;
//       });
//   } else if(step == 2){
//     header.textContent = "Add outfits";
//     nextButton.textContent = "Create";

//     fetch(`/showrooms/${showroomId}/select-outfits/`)
//       .then(res => res.text())
//       .then(html => {
//         modalContent.innerHTML = html;
//       });
//   }
// }

// document.getElementById('modal-next-button').addEventListener('click', () => {
//   if (currentStep === 1) {
//     // form validation (?)






