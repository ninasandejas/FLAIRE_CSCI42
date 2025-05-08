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