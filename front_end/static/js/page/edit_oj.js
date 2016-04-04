$(document).ready(function() {
  $("#btn-edit-oj").click(function() {
    var data = {}

    data.name = $("#input-name").val();
    data.caption = $("#input-caption").val();

    if ($("input[name='radio-status']:checked").val() == "available") {
      data.available = true;
    } else {
      data.available = false;
    }

    data.crawler_problem = $("#input-crawler-problem").val();
    data.crawler_submission = $("#input-crawler-submission").val();
    data.crawler_category = $("#input-crawler-category").val();

    $.ajax({
      type: "POST",
      url: "/api/oj/modify/",
      async: false,
      data: data,
      dataType: "text",
      success: function(response) {
        if (response == "SUCCESS") {
          location.href = location.href = document.referrer;
        } else if (response == "OJ_NOT_EXISTS") {
          $("#div-form-group-name").addClass("has-error");
          $("#h-head").addClass("text-danger").text("OJ not exists.");
        } else {
          $("#div-form-group-name").addClass("has-error");
          $("#h-head").addClass("text-danger").text("Name or caption can't be empty.")
        }
      }
    });
  });

  $("#btn-delete-oj").click(function() {
    if (window.confirm('Are you sure to delete this OJ?')) {
      name = $("#input-name").val();

      $.ajax({
        type: "POST",
        url: "/api/oj/delete/",
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