$(document).ready(function() {
  $("#a-user-menu-sign-out").click(function() {
    $.ajax({
      type: "POST",
      url: "/api/user/logout/",
      async: false,
      dataType: "text",
      success: function(response) {
        if (response == 'SUCCESS') {
          location.reload();
        } else {
          alert(response);
        }
      }
    });
  });

  $("#btn-search-user").click(function() {
    var value = $("#input-search-user").val();
    if (value != "") {
      location.href = "/user/search/"+value+"/0/50/";
    }
  });
});