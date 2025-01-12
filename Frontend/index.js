document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll(".header .background-image");
    let currentIndex = 0;
  
    function fadeInOut() {
      // Reset opacity of all images
      images.forEach((image) => {
        image.classList.remove("active");
      });
  
      // Set the current image as visible
      images[currentIndex].classList.add("active");
  
      // Move to the next image
      currentIndex = (currentIndex + 1) % images.length;
    }
  
    // Change image every 5 seconds
    setInterval(fadeInOut, 5000);
  
    // Initial call
    fadeInOut();
  });
  