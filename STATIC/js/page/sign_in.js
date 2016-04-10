$(document).ready(function() {
  $("#btn-sign-in").click(function() {
    var username = $("#input-username").val();
    var password = $("#input-password").val();

    $.ajax({
      type: "POST",
      url: "/api/user/login/",
      async: false,
      dataType: "text",
      data: {
        "username": username,
        "password": password
      },
      success: function(response) {
        if (response == 'SUCCESS') {
          location.href = location.href = document.referrer;
        } else if (response == 'USERNAME_OR_PASSWORD_WRONG') {
          $("#p-username-password-wrong").removeAttr("hidden");
          $("#div-form-group-username").addClass("has-error");
          $("#div-form-group-password").addClass("has-error");
        } else {
          alert("Sorry, your account has been frozen. You have no permission to login.");
        }
      }
    });
  });
});