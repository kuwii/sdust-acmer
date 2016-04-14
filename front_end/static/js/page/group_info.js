$(document).ready(function() {
  var target_user = $('#target-user').text();
  var self_user = $('#self-user').text();

  $("#div-basic").show();
  $("#div-members").hide();
  $("#div-categories").hide();
  $("#li-show-basic").addClass("active");

  $("#btn-show-basic").click(function() {
    $("#div-basic").show();
    $("#li-show-basic").addClass("active");
    $("#div-members").hide();
    $("#li-show-members").removeClass("active");
    $("#div-categories").hide();
    $("#li-show-categories").removeClass("active");
  });

  $("#btn-show-members").click(function() {
    $("#div-members").show();
    $("#li-show-members").addClass("active");
    $("#div-basic").hide();
    $("#li-show-basic").removeClass("active");
    $("#div-categories").hide();
    $("#li-show-categories").removeClass("active");
  });

  $("#btn-show-categories").click(function() {
    $("#div-categories").show();
    $("#li-show-categories").addClass("active");
    $("#div-members").hide();
    $("#li-show-members").removeClass("active");
    $("#div-basic").hide();
    $("#li-show-basic").removeClass("active");
  });

  $("#btn-update-basic").click(function() {
    if($(this).hasClass("disabled")) return;

    var username = $("#target-user").text();

    $(this).addClass("disabled").text("Updating ...");
    alert("Upgrade starts.");

    $.ajax({
      type: "POST",
      url: "/api/basic/update/",
      async: true,
      data: {
        "username": username
      },
      dataType: "text",
      success: function(response) {
        alert(response);
        location.reload();
      }
    });
  });

  $("#btn-follow-user").click(function() {
    $.ajax({
      type: 'POST',
      url: '/api/user/follow/',
      data: {
        'username': target_user
      },
      dataType: 'text',
      success: function(response) {
        if (response == "SUCCESS") {
          location.reload();
        } else {
          alert(response);
        }
      }
    });
  });

  $("#btn-unfollow-user").click(function() {
    $.ajax({
      type: 'POST',
      url: '/api/user/unfollow/',
      data: {
        'username': target_user
      },
      dataType: 'text',
      success: function(response) {
        if (response == "SUCCESS") {
          location.reload();
        } else {
          alert(response);
        }
      }
    });
  });

  $("#btn-join-group").click(function() {
    $.ajax({
      type: 'POST',
      url: '/api/group/join/',
      data: {
        'name': $("#group-name").text()
      },
      dataType: 'text',
      success(response) {
        if(response == "SUCCESS") {
          location.reload();
        } else if (response == "IS_ALREADY_APPLICANT") {
          alert("You are already applicant, Please wait for the manager to approve.");
        } else {
          alert(response);
        }
      }
    });
  });

  $("#btn-approve-user").click(function() {
    $.ajax({
      type: 'POST',
      url: '/api/group/approve/',
      data: {
        'name': $("#group-name").text(),
        'username': $(this).parent().parent().parent().children(".applicant-username").text()
      },
      dataType: 'text',
      success(response) {
        if(response == "SUCCESS") {
          location.reload();
        } else {
          alert(response);
        }
      }
    });
  });

  $("#btn-leave-group").click(function() {
    if(confirm("Are you sure to leave this group? Notice that if you leave a private group, you still need to be approved again if you want to join the group again.")) {
      $.ajax({
        type: 'POST',
        url: '/api/group/leave/',
        data: {
          'name': $("#group-name").text(),
        },
        dataType: 'text',
        success(response) {
          if(response == "SUCCESS") {
            location.reload();
          } else {
            alert('You are the boss of the group, who must not leave the group.');
          }
        }
      });
    }
  });

  $("#btn-kick-user").click(function() {
    if(confirm("Are you sure to kick this user out of this group?")) {
      $.ajax({
        type: "post",
        url: "/api/group/kick/",
        data: {
          'name': $("#group-name").text(),
          'username': $(this).parent().parent().parent().children(".member-username").text()
        },
        dataType: "text",
        success: function(response) {
          if(response == "SUCCESS") {
            location.reload();
          } else if (response == "CANNOT_KICK_MANAGER") {
            alert("Well, only the boss can kick manager, you can't.")
          }
        }
      });
    }
  })
});