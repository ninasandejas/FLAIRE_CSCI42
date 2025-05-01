document.addEventListener('DOMContentLoaded', () => {
    const wishlistItems = JSON.parse(document.getElementById('wishlist-data').textContent);

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