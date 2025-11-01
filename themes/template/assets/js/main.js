document.addEventListener('DOMContentLoaded', function() {
  const hamburgerToggle = document.getElementById('hamburger-toggle');
  const hamburgerNav = document.getElementById('hamburger-nav');
  const hamburgerIcon = document.getElementById('hamburger-icon');

  if (hamburgerToggle && hamburgerNav && hamburgerIcon) {
    hamburgerToggle.addEventListener('click', function() {
      const isOpen = hamburgerNav.classList.toggle('open');
      
      if (isOpen) {
        hamburgerIcon.classList.remove('fa-bars');
        hamburgerIcon.classList.add('fa-x');
      } else {
        hamburgerIcon.classList.remove('fa-x');
        hamburgerIcon.classList.add('fa-bars');
      }
    });
  }
});

