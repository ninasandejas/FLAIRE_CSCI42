document.addEventListener('DOMContentLoaded', function () {
  const followersModal = document.getElementById('followers-following-modal');
  const modalTitle = document.getElementById('modal-title');
  const modalUserList = document.getElementById('modal-user-list');
  const closeModal = document.querySelector('.close-modal');
  const profileStats = document.querySelector('.profile-stats');
  const username = profileStats.dataset.username;
  const loggedInUsername = document.querySelector('meta[name="username"]').content;

  function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  }

  function openModal(title, users) {
    modalTitle.textContent = title;
    modalUserList.innerHTML = '';
    if (users.length === 0) {
      const noUsersItem = document.createElement('div');
      noUsersItem.textContent = 'No users';
      noUsersItem.classList.add('no-users');
      modalUserList.appendChild(noUsersItem);
    } else {
      users.forEach(user => {
        const listItem = document.createElement('div');
        listItem.classList.add('user-item');

        const link = document.createElement('a');
        link.href = `/profile/${user.username}/`;
        link.classList.add('username');

        const profilePic = document.createElement('img');
        profilePic.src = user.profile_picture_url || '/static/img/user-icon.png';
        profilePic.alt = `${user.username}'s profile picture`;
        profilePic.classList.add('profile-pic-small');

        const usernameSpan = document.createElement('span');
        usernameSpan.textContent = user.username;
        usernameSpan.classList.add('username');

        link.appendChild(profilePic);
        link.appendChild(usernameSpan);
        listItem.appendChild(link);

        if (user.username !== loggedInUsername) {
          const followButton = document.createElement('button');
          followButton.type = 'button';
          followButton.classList.add('follow-unfollow-btn'); // Use the existing follow button CSS
          followButton.textContent = user.follow_status === 'Unfollow' ? 'Unfollow' : 'Follow';
          followButton.addEventListener('click', () => {
            fetch(`/api/follow/${user.username}/`, {
              method: 'POST',
              headers: {
                'X-CSRFToken': getCSRFToken(),
              },
            })
              .then(response => {
                if (!response.ok) {
                  throw new Error('Failed to toggle follow status');
                }
                return response.json();
              })
              .then(data => {
                followButton.textContent = data.new_status;
                user.follow_status = data.new_status; // Update the user's follow status
              })
              .catch(error => {
                console.error('Error:', error);
              });
          });

          listItem.appendChild(followButton);
        }

        modalUserList.appendChild(listItem);
      });
    }
    followersModal.style.display = 'block';
  }

  closeModal.addEventListener('click', () => {
    followersModal.style.display = 'none';
  });

  window.addEventListener('click', (event) => {
    if (event.target === followersModal) {
      followersModal.style.display = 'none';
    }
  });

  const followersStat = document.querySelector('.profile-stats .stat-item:nth-child(1)');
  const followingStat = document.querySelector('.profile-stats .stat-item:nth-child(2)');

  if (followersStat) {
    followersStat.addEventListener('click', (event) => {
      const count = event.target.dataset.count;
      fetch(`/api/followers/${username}/`)
        .then(response => response.json())
        .then(data => openModal('Followers', data));
    });
  } else {
    console.error('Followers stat element not found.');
  }

  if (followingStat) {
    followingStat.addEventListener('click', (event) => {
      const count = event.target.dataset.count;
      fetch(`/api/following/${username}/`)
        .then(response => response.json())
        .then(data => openModal('Following', data));
    });
  } else {
    console.error('Following stat element not found.');
  }
});