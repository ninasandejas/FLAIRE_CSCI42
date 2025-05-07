const grid = document.getElementById('outfits-grid');
const showroomId = grid.dataset.showroomId;


// dynamically loads the outfits of the showroom
document.addEventListener('DOMContentLoaded', () => {
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


// editing of showromm: for now, only edits the title but i'll soon 
// find a way to have it be a way to organize outfit order
document.addEventListener('DOMContentLoaded', () => {
  const editButton = document.getElementById('edit-button');
  const h3 = document.getElementById('showroom-title');
  const input = document.getElementById('edit-title');
  
  if (!editButton || !h3 || !input) return;

  editButton.addEventListener('click', () => {
    const state = editButton.dataset.state;

    if (state === 'edit') {
      input.value = h3.textContent;
      h3.style.display = 'none';
      input.style.display = 'inline-block';
      editButton.textContent = 'Save';
      editButton.dataset.state = 'save'
      input.focus();
    } 
    else if (state === 'save') {
      const newTitle = input.value.trim();

      fetch(`/showrooms/${showroomId}/update/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ title: newTitle })
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          h3.textContent = newTitle;
          input.style.display = 'none';
          h3.style.display = 'block';
          editButton.textContent = 'Edit';
          editButton.dataset.state = 'edit';
        } else {
          alert('Failed to update title.');
        }
      })
      .catch(err => {
        console.error(err);
        alert('Error occurred during update.');
      });
    }

  });
});


// follow button:
document.addEventListener('DOMContentLoaded', () => {
  const followButton = document.getElementById('follow-button');

  if (!followButton) return; 

  followButton.addEventListener('click', () => {
    fetch(`/showrooms/${showroomId}/follow/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({})
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        document.getElementById('follower-count').textContent = data.new_follower_count;
  
        document.getElementById('follow-button').textContent = "Following";
        document.getElementById('follow-button').disabled = true;
      } else {
        alert("Something went wrong.");
      }
    });
  });

});


// accept incoming invite for showroom collaborator
document.addEventListener('DOMContentLoaded', () => {
  const acceptButton = document.getElementById('accept-button');

  if (!acceptButton) return; 

  acceptButton.addEventListener('click', () => {
    fetch(`/showrooms/${showroomId}/accept/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({})
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        window.location.reload();
      } else {
        alert("Something went wrong.");
      }
    });
  });

});

// add outfits in showroom detail
document.addEventListener("DOMContentLoaded", function () {
  var modal = document.getElementById("create-sr-add-outfits");
  var btn = document.getElementById("add-outfits-btn-dt");
  var span = document.getElementsByClassName("close")[0];
  
  btn.onclick = function() {
    modal.style.display = "block";
    btn.disabled = true;
    loadOutfits();
  }

  span.onclick = function() {
    modal.style.display = "none";
    btn.disabled = false;
  }

  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
      btn.disabled = false;
    }
  }
});

// loading of outfits in add outfit modal
const container = document.getElementById('add-outfits-sr-content');
function loadOutfits() {
  container.innerHTML = '';
  fetch(`/showrooms/${showroomId}/add-outfits/`)
    .then(res => res.json())
    .then(data => {
      data.outfits.forEach(outfit => {
        const img = document.createElement('img');
        img.src = outfit.image;
        img.alt = `Outfit ${outfit.id}`;

        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'outfit-as-btn';
        button.dataset.outfitId = outfit.id;

        button.appendChild(img);
        container.appendChild(button);

        button.addEventListener('click', () => {
          addOutfitToShowroom(outfit.id);
        });
      })
    });
}


function addOutfitToShowroom(outfitId) {
  fetch(`/showrooms/${showroomId}/add-outfit/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({ outfit_id: outfitId })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      alert('Outfit added!');
    } else {
      alert('Failed to add outfit.');
    }
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
