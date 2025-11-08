// Reading progress bar
(function() {
  'use strict';

  function initReadingProgress() {
    const progressBar = document.getElementById('reading-progress');
    if (!progressBar) return;

    // Only show on posts and pages
    const isPost = document.querySelector('.post');
    const isPage = document.querySelector('.page');
    if (!isPost && !isPage) {
      progressBar.style.display = 'none';
      return;
    }

    let ticking = false;

    function updateProgress() {
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight;
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const scrollableHeight = documentHeight - windowHeight;
      const progress = scrollableHeight > 0 ? (scrollTop / scrollableHeight) * 100 : 0;

      progressBar.style.width = Math.min(progress, 100) + '%';
      ticking = false;
    }

    function requestTick() {
      if (!ticking) {
        window.requestAnimationFrame(updateProgress);
        ticking = true;
      }
    }

    // Update on scroll
    window.addEventListener('scroll', requestTick, { passive: true });
    
    // Update on resize
    window.addEventListener('resize', requestTick, { passive: true });
    
    // Initial update
    updateProgress();
  }

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initReadingProgress);
  } else {
    initReadingProgress();
  }
})();

// Progressive loading for post cover and book cover images
(function() {
  'use strict';

  function initProgressiveImages() {
    // Handle post cover images
    const postCoverImg = document.querySelector('.post-cover-img');
    if (postCoverImg) {
      handleImageLoad(postCoverImg);
    }

    // Handle book cover images
    const bookCoverImages = document.querySelectorAll('.book-cover-img');
    bookCoverImages.forEach(function(img) {
      handleImageLoad(img);
    });
  }

  function handleImageLoad(img) {
    function markLoaded() {
      img.classList.add('loaded');
    }

    // If image is already loaded (cached), show it immediately without transition
    if (img.complete && img.naturalHeight !== 0) {
      img.style.transition = 'none';
      markLoaded();
    } else {
      img.addEventListener('load', markLoaded);
    }
  }

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initProgressiveImages);
  } else {
    initProgressiveImages();
  }
})();

// Slide viewer with Glide.js
(function() {
  'use strict';

  function initSlideViewer() {
    const slideViewer = document.querySelector('.slide-viewer');
    if (!slideViewer) return;

    // Check if Glide is available
    if (typeof Glide === 'undefined') {
      console.warn('Glide.js is not loaded');
      return;
    }

    const glideElement = slideViewer.querySelector('.glide');
    if (!glideElement) return;

    const slideCount = parseInt(slideViewer.dataset.slideCount, 10) || 0;
    const currentSlideEl = slideViewer.querySelector('.slide-counter__current');
    const totalSlideEl = slideViewer.querySelector('.slide-counter__total');

    // Initialize Glide
    const glide = new Glide(glideElement, {
      type: 'carousel',
      startAt: 0,
      perView: 1,
      gap: 0,
      keyboard: true,
      animationDuration: 400,
      animationTimingFunc: 'ease-in-out',
      swipeThreshold: 80,
      dragThreshold: 120,
    });

    // Update slide counter
    function updateCounter() {
      if (currentSlideEl) {
        currentSlideEl.textContent = glide.index + 1;
      }
    }

    // Listen to slide changes
    glide.on(['mount.after', 'run'], function() {
      updateCounter();
    });

    // Mount Glide
    glide.mount();

    // Update counter on initial mount
    updateCounter();
  }

  // Initialize on DOM ready, wait for Glide to be available
  function tryInit() {
    if (typeof Glide !== 'undefined') {
      initSlideViewer();
    } else {
      // Retry if Glide hasn't loaded yet
      setTimeout(tryInit, 50);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', tryInit);
  } else {
    tryInit();
  }
})();

