document.addEventListener('DOMContentLoaded', () => {
    const ootdModal = document.getElementById('ootd-modal');
    const addOotdBtn = document.getElementById('add-ootd-btn');
    const manageOotdBtn = document.getElementById('manage-ootd-btn');
    const closeModal = ootdModal.querySelector('.close-modal');

    if (addOotdBtn) {
      addOotdBtn.addEventListener('click', () => {
        ootdModal.style.display = 'block';
      });
    }

    if (manageOotdBtn) {
      manageOotdBtn.addEventListener('click', (e) => {
        e.preventDefault();
        ootdModal.style.display = 'block';
      });
    }

    closeModal.addEventListener('click', () => {
      ootdModal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
      if (e.target === ootdModal) {
        ootdModal.style.display = 'none';
      }
    });

    const wishlistItems = [
      ...JSON.parse(document.getElementById('wishlist-data').textContent)
    ];

    const wishlistImage = document.getElementById('wishlist-main-image');
    const prevButton = document.querySelector('.wishlist-nav-prev');
    const nextButton = document.querySelector('.wishlist-nav-next');

    let currentIndex = 0;

    const updateWishlistImage = () => {
      if (wishlistItems.length > 0) {
        wishlistImage.src = wishlistItems[currentIndex].image;
        wishlistImage.alt = wishlistItems[currentIndex].name;
      }
    };

    prevButton.addEventListener('click', () => {
      currentIndex = (currentIndex - 1 + wishlistItems.length) % wishlistItems.length;
      updateWishlistImage();
    });

    nextButton.addEventListener('click', () => {
      currentIndex = (currentIndex + 1) % wishlistItems.length;
      updateWishlistImage();
    });

    updateWishlistImage();
});