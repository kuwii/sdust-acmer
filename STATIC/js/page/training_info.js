$(document).ready(function() {
  var target_user = $('#target-user').text();
  var self_user = $('#self-user').text();

  $("#div-submissions").show();
  $("#div-problems").hide();
  $("#div-categories").hide();
  $("#li-show-submissions").addClass("active");

  $.ajax({
    type: "GET",
    url: "/user/submissions/get/"+target_user+"/",
    async: true,
    dataType: "html",
    success: function(response) {
      $("#div-submissions").removeClass("jumbotron").append(response);

      calculate_time();
      $(".calculate-time").removeClass("calculate-time");

      $("#h-div-submissions-loading").remove();
    }
  })

  $.ajax({
    type: "GET",
    url: "/user/problems/get/"+target_user+"/",
    async: true,
    dataType: "html",
    success: function(response) {
      $("#div-problems").removeClass("jumbotron").append(response);

      calculate_time();
      $(".calculate-time").removeClass("calculate-time");

      $("#h-div-problems-loading").remove();
    }
  })

  $("#btn-show-submissions").click(function() {
    $("#div-submissions").show();
    $("#li-show-submissions").addClass("active");
    $("#div-problems").hide();
    $("#li-show-problems").removeClass("active");
    $("#div-categories").hide();
    $("#li-show-categories").removeClass("active");
  });

  $("#btn-show-problems").click(function() {
    $("#div-problems").show();
    $("#li-show-problems").addClass("active");
    $("#div-submissions").hide();
    $("#li-show-submissions").removeClass("active");
    $("#div-categories").hide();
    $("#li-show-categories").removeClass("active");
  });

  $("#btn-show-categories").click(function() {
    $("#div-categories").show();
    $("#li-show-categories").addClass("active");
    $("#div-problems").hide();
    $("#li-show-problems").removeClass("active");
    $("#div-submissions").hide();
    $("#li-show-submissions").removeClass("active");
  });

  $("#btn-update-submissions").click(function() {
    if($(this).hasClass("disabled")) return;

    var username = $("#target-user").text();

    $(this).addClass("disabled").text("Updating ...");
    alert("Upgrade starts.");

    $.ajax({
      type: "POST",
      url: "/api/submissions/update/",
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
});