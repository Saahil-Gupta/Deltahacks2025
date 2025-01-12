document.addEventListener("DOMContentLoaded", function() {
    const images = document.querySelectorAll('.header .background-image');
    let currentIndex = 0;

    function fadeInOut() {
        // Set opacity of all images to 0
        images.forEach(image => {
            image.style.opacity = 0;
        });

        // Set the current image to be visible
        images[currentIndex].style.opacity = 1;

        // Move to the next image in the sequence
        currentIndex = (currentIndex + 1) % images.length; // Cycle through images
    }

    // Change image every 5 seconds
    setInterval(fadeInOut, 5000);

    // Initial call to show the first image
    fadeInOut();
});
