$(document).ready(function() {
  $("#btn-show-joined").click(function() {
    $("#tbody-joined").removeAttr("hidden");
    $("#tbody-pending").attr("hidden", "hidden");
    $("#li-show-joined").addClass("active");
    $("#li-show-pending").removeClass("active");
  });

  $("#btn-show-pending").click(function() {
    $("#tbody-pending").removeAttr("hidden");
    $("#tbody-joined").attr("hidden", "hidden");
    $("#li-show-pending").addClass("active");
    $("#li-show-joined").removeClass("active");
  });
});