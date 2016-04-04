$(document).ready(function() {
  $("#btn-sign-in").click(function() {
    $("#input-username").removeClass("has-error");
    $("#input-password").removeClass("has-error");
    $("#input-confirm").removeClass("has-error");

    var username = $("#input-username").val();
    var password = $("#input-password").val();
    var confirm = $("#input-confirm").val();

    if (password == confirm) {
      $.ajax({
        type: "POST",
        url: "/api/user/register/",
        async: false,
        dataType: "text",
        data: {
          "username": username,
          "password": password
        },
        success: function(response) {
          if (response == 'SUCCESS') {
            location.href = location.href = document.referrer;
          } else if (response == 'INVALID_USER_NAME') {
            $("#p-error-info").removeAttr("hidden").text("Username can only contain letters, numbers and underscores");
            $("#div-form-group-username").addClass("has-error");
          } else if (response == 'USER_EXISTS') {
            $("#p-error-info").removeAttr("hidden").text("User exists.");
            $("#div-form-group-username").addClass("has-error");
          }
        }
      });
    } else {
      $("#p-error-info").removeAttr("hidden").text("Password confirmation failed.");
      $("#div-form-group-password").addClass("has-error");
      $("#div-form-group-confirm").addClass("has-error");
    }
  });
});