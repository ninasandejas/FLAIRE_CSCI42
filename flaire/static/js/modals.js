document.addEventListener('DOMContentLoaded', () => {

    const modals = document.querySelectorAll('.modal');
    const editProfileModal = document.getElementById('edit-profile-modal');
    const ootdModal = document.getElementById('ootd-modal');

    const editIcon = document.querySelector('.edit-icon');
    const addOotdBtn = document.getElementById('add-ootd-btn');
    const manageOotdBtn = document.getElementById('manage-ootd-btn');

    const closeModalButtons = document.querySelectorAll('.close-modal');

    if (editIcon) {
      editIcon.addEventListener('click', (e) => {
        e.preventDefault();
        editProfileModal.style.display = 'block';
      });
    }

    if (addOotdBtn) {
      addOotdBtn.addEventListener('click', () => {
        ootdModal.style.display = 'block';
      });
    }

    if (manageOotdBtn) {
      manageOotdBtn.addEventListener('click', () => {
        ootdModal.style.display = 'block';
      });
    }

    closeModalButtons.forEach((button) => {
      button.addEventListener('click', () => {
        modals.forEach((modal) => {
          modal.style.display = 'none';
        });
      });
    });

    window.addEventListener('click', (e) => {
      modals.forEach((modal) => {
        if (e.target === modal) {
          modal.style.display = 'none';
        }
      });
    });
});