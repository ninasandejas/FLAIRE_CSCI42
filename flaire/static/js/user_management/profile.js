document.addEventListener('DOMContentLoaded', () => {
    const wishlistItems = JSON.parse(document.getElementById('wishlist-data').textContent);

    console.log('Wishlist Items:', wishlistItems); // Debugging log

    const wishlistImage = document.getElementById('wishlist-main-image');
    const prevButton = document.querySelector('.wishlist-nav-prev');
    const nextButton = document.querySelector('.wishlist-nav-next');

    let currentIndex = 0;

    const updateWishlistImage = () => {
      if (wishlistItems.length > 0) {
        console.log('Updating image to:', wishlistItems[currentIndex]); // Debugging log
        wishlistImage.src = wishlistItems[currentIndex].image;
        wishlistImage.alt = wishlistItems[currentIndex].name;
      }
    };

    prevButton.addEventListener('click', () => {
      currentIndex = (currentIndex - 1 + wishlistItems.length) % wishlistItems.length;
      console.log('Previous button clicked. Current index:', currentIndex); // Debugging log
      updateWishlistImage();
    });

    nextButton.addEventListener('click', () => {
      currentIndex = (currentIndex + 1) % wishlistItems.length;
      console.log('Next button clicked. Current index:', currentIndex); // Debugging log
      updateWishlistImage();
    });

    updateWishlistImage();
});