$(document).ready(function() {

  $(".btn-update-problems").click(function () {
    if($(this).hasClass("disabled")) return;

    var oj_name = $(this).parent().parent().children(".oj-name").text();

    $(this).addClass("disabled").text("Updating ...");
    alert("Upgrade starts.");

    $.ajax({
      type: "POST",
      url: "/api/problems/update/",
      async: true,
      data: {
        "oj_name": oj_name
      },
      dataType: "text",
      async: false,
      success(response) {
        if (response == "SUCCESS") {
          alert("Succeeded");
          location.reload();
        } else if (response == "OJ_UPDATING") {
          alert("This OJ is already updating.");
        } else {
          alert(response);
        }
      }
    });
  });
});