$(document).ready(function() {
  $(".category").click(function() {
    $(this).after(
    "<ul>"+
      "<li>"+
        "<span class=\"category\">Grand Child</span> <a href=\"\">Goes somewhere</a>"+
      "</li>"+
    "</ul>"
    );
  });
});