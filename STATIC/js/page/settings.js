$(document).ready(function() {
  var target_user = $("#target-user").text();

  $("#btn-save-personal-info").click(function() {
    var data = {"username": target_user};

    var nickname = $("#input-nickname").val();
    if (nickname == "") {
      nickname = null;
    }
    data.nickname = nickname;

    data.sex = $("input[name='radio-user-sex']:checked").val();

    var school = $("#input-school").val();
    if (school == "") school = null;
    data.school = school;

    $.ajax({
      type: "POST",
      url: "/api/user/modify/",
      async: false,
      data: data,
      dataType: "text",
      success: function(response) {
        if (response == 'SUCCESS') {
          $("#btn-save-personal-info").removeClass("btn-primary").addClass("btn-success");
          $("#h-personal-information").addClass("text-success").text("Personal information saved.");
        }
      }
    });
  });

  $("#btn-save-password").click(function() {
    var new_password = $("#input-new-password").val();
    if (new_password != "") {
      var data = {"username": target_user};
      var confirm = $("#input-confirm").val();

      if (new_password != confirm) {
        $("#div-form-group-new-password").addClass("has-error");
        $("#div-form-group-confirm").addClass("has-error");
        $("#h-change-password").addClass("text-danger").text("Password confirmation failed.");
      } else {
        data.new_password = new_password;
        $old_exists = $("#input-old-password").attr("disabled");
        if (typeof($old_exists) == "undefined") data.old_password = $("#input-old-password").val();

        $.ajax({
          type: "POST",
          url: "/api/user/change-password/",
          async: false,
          data: data,
          dataType: "text",
          success: function(response) {
            alert(response);

            if (response == "SUCCESS") {
              $("#btn-save-password").removeClass("btn-primary").addClass("btn-success");
              $("#h-change-password").addClass("text-success").text("Password has been changed.");

              if (typeof($old_exists) == "undefined") {
                $.ajax({
                  type: "POST",
                  url: "/api/user/logout/",
                  dataType: "text",
                  success: function(response) {
                    location.reload();
                  }
                });
              }
            } else if (response == "USERNAME_OR_PASSWORD_WRONG") {
              $("#div-form-group-old-password").addClass("has-error");
              $("#h-change-password").addClass("text-danger").text("Wrong old password");
            }
          }
        });
      }

    }
  });

  $("#btn-add-new-account").click(function() {
    var oj_name = $("#select-new-account-oj").val();
    var account = $("#input-new-account-account").val();

    var data = {
      "oj_name": oj_name,
      "username": target_user,
      "account": account
    };

    $.ajax({
      type: "POST",
      url: "/api/accounts/create/",
      async: false,
      data: data,
      dataType: "text",
      success: function(response) {
        if (response == "SUCCESS") {
          location.reload();
        } else {
          $("#h-new-account").addClass("text-danger").text("Accounts Exists");
        }
      }
    });
  });

  $(".btn-delete-account").click(function() {
    var oj_name = $(this).parent().parent().children(".id-oj-name").text();

    var data = {
      "oj_name": oj_name,
      "username": target_user
    }

    if (window.confirm("Sure to delete this account? All your information related to this account, such as your submissions and your solved problems, will be deleted.")) {
      $.ajax({
        type: "POST",
        url: "/api/accounts/delete/",
        async: false,
        data: data,
        dataType: "text",
        success: function(response) {
          if (response == "SUCCESS") {
            location.reload();
          } else {
            alert("Unknown error occurred.");
          }
        }
      });
    }
  });
});