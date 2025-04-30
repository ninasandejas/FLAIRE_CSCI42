document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded and parsed'); // Debugging log

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
        console.log('Edit Profile button clicked'); // Debugging log
        editProfileModal.style.display = 'block';
      });
    }

    if (addOotdBtn) {
      addOotdBtn.addEventListener('click', () => {
        console.log('Add OOTD button clicked'); // Debugging log
        ootdModal.style.display = 'block';
      });
    }

    if (manageOotdBtn) {
      manageOotdBtn.addEventListener('click', () => {
        console.log('Manage OOTD button clicked'); // Debugging log
        ootdModal.style.display = 'block';
      });
    }

    closeModalButtons.forEach((button) => {
      button.addEventListener('click', () => {
        console.log('Close button clicked'); // Debugging log
        modals.forEach((modal) => {
          modal.style.display = 'none';
        });
      });
    });

    window.addEventListener('click', (e) => {
      modals.forEach((modal) => {
        if (e.target === modal) {
          console.log('Clicked outside modal'); // Debugging log
          modal.style.display = 'none';
        }
      });
    });
});