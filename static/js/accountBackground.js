window.addEventListener('load', () => {
    const coolElement = document.querySelector('.cool');
    const startPositionY = 10; // Initial gradient position
    const endPositionY = 90; // Final gradient position
    const duration = 4000; // Animation duration in milliseconds
    const frameRate = 60; // Frames per second
    const totalFrames = (duration / 1000) * frameRate;

    let frame = 0;

    // Disable scrolling
    document.body.style.overflow = 'hidden';
    document.documentElement.style.overflow = 'hidden';

    // Ease-in-out function
    const easeInOut = (t) => {
        return t < 0.5
            ? 2 * t * t
            : 1 - Math.pow(-2 * t + 2, 2) / 2;
    };

    const animateGradient = () => {
        const progress = frame / totalFrames; // Normalized progress (0 to 1)
        const easedProgress = easeInOut(progress); // Apply easing

        // Interpolate the Y position based on eased progress
        const positionY = startPositionY + easedProgress * (endPositionY - startPositionY);

        coolElement.style.background = `radial-gradient(
            125% 125% at 50% ${positionY}%, 
            #000 40%, 
            rgb(0, 13, 255) 100%
        )`;

        frame++;

        if (frame < totalFrames) {
            requestAnimationFrame(animateGradient);
        } else {
            // Re-enable scrolling after the animation is complete
            document.body.style.overflow = '';
            document.documentElement.style.overflow = '';
        }
    };

    // Delay the animation by 0.5 seconds
    setTimeout(() => {
        requestAnimationFrame(animateGradient);
    }, 500);

    const p = document.getElementById('p-fade');

    // Add the opacity class after a small delay (if desired)
    setTimeout(() => {
        p.classList.remove('opacity-0'); // Remove initial opacity-0
        p.classList.add('opacity-100'); // Add full opacity
    }, 900); 
});


document.addEventListener('DOMContentLoaded', () => {
    const section = document.getElementById('content-section-1');

    // Check if the element exists to avoid null errors
    if (section) {
        // Add the fade-in class to the section initially
        section.classList.add('fade-in');

        // Scroll event listener
        window.addEventListener('scroll', () => {
            const sectionRect = section.getBoundingClientRect();
            const viewportHeight = window.innerHeight;
            const threshold = viewportHeight * 0.05; // 5vh equivalent

            // Check if the section is within the threshold
            if (sectionRect.top <= viewportHeight - threshold) {
                section.classList.add('visible'); // Add visible class to trigger fade-in
            }
        });
    } else {
        console.error("Element with ID 'content-section-1' not found.");
    }
});