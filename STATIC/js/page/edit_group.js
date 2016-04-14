$(document).ready(function() {
  $("#btn-edit-group").click(function() {
    var data = {}

    data.name = $("#input-group-name").val();
    data.caption = $("#input-group-caption").val();
    data.public = $("input[name='radio-group-public']:checked").val();
    data.introduction = $("#input-group-introduction").val();

    $.ajax({
      type: "POST",
      url: "/api/group/modify/",
      async: false,
      data: data,
      dataType: "text",
      success: function(response) {
        if (response == "SUCCESS") {
          location.href = location.href = document.referrer;
        } else {
          alert(response);
        }
      }
    });
  });


  $("#btn-delete-group").click(function() {
    if (window.confirm('Are you sure to delete this OJ?')) {
      name = $("#input-group-name").val();

      $.ajax({
        type: "POST",
        url: "/api/group/delete/",
        async: false,
        data: {"name": name},
        dataType: "text",
        success: function(response) {
          if (response == "SUCCESS") {
            location.href = location.href = document.referrer;
          } else {
            alert(response);
          }
        }
      });
    }
  });
});