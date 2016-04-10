$(document).ready(function() {
  $("#btn-show-following").click(function() {
    $("#tbody-following").removeAttr("hidden");
    $("#tbody-followers").attr("hidden", "hidden");
    $("#li-show-following").addClass("active");
    $("#li-show-followers").removeClass("active");
  });

  $("#btn-show-followers").click(function() {
    $("#tbody-followers").removeAttr("hidden");
    $("#tbody-following").attr("hidden", "hidden");
    $("#li-show-followers").addClass("active");
    $("#li-show-following").removeClass("active");
  });
});