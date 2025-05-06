// let currentPage = 1;

// document.getElementById('add-outfits-btn').addEventListener('click', function () {
//   currentPage = 1;
//   loadOutfits(currentPage);
//   const modal = new bootstrap.Modal(document.getElementById('outfitsModal'));
//   modal.show();
// });

// document.getElementById('load-more').addEventListener('click', function () {
//   currentPage += 1;
//   loadOutfits(currentPage, true); // Append instead of replace
// });

// function loadOutfits(page = 1, append = false) {
//   fetch(`/showrooms/add-outfits/?page=${page}`)
//     .then(response => response.text())
//     .then(html => {
//       const container = document.getElementById('outfit-container');
//       if (append) {
//         container.innerHTML += html;
//       } else {
//         container.innerHTML = html;
//       }
//     });
// }


document.addEventListener("DOMContentLoaded", function () {
  var modal = document.getElementById("create-sr-add-outfits");
  var btn = document.getElementById("add-outfits-btn");
  var span = document.getElementsByClassName("close")[0];
  
  btn.onclick = function() {
    modal.style.display = "block";
    loadOutfits();
  }

  span.onclick = function() {
    modal.style.display = "none";
  }

  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
});

const container = document.getElementById('add-outfits-sr-content');
function loadOutfits() {
  fetch(`/showrooms/add-outfits/`)
    .then(res => res.json())
    .then(data => {
      data.outfits.forEach(outfit => {
        const img = document.createElement('img');
        img.src = outfit.image;
        img.alt = `Outfit ${outfit.id}`;

        container.appendChild(img);
      })
    });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}