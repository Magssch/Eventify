
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.dropdown-trigger');
    var options = {};

    var instances = M.Dropdown.init(elems, options);
  });

document.addEventListener('DOMContentLoaded', function () {
  var elems = document.querySelectorAll('.slider');
  var options = {};

  var instances = M.Slider.init(elems, height = "400", duration = "500", interval = "600");
});


document.addEventListener('DOMContentLoaded', function () {
  var elems = document.querySelectorAll('.autocomplete');
  var options = {};

  var instances = M.Autocomplete.init(elems, options);
});

document.addEventListener('DOMContentLoaded', function() {
var elems = document.querySelectorAll('.sidenav');
var options = {};

var instances = M.Sidenav.init(elems, options);
});