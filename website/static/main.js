document.addEventListener('DOMContentLoaded', function () {
    var navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
    if (navbarBurgers.length > 0) {
      navbarBurgers.forEach(function (el) {
        el.addEventListener('click', function () {
          var target = document.getElementById('main-nav');
          target.classList.toggle('hidden');
        });
      });
    }
  });