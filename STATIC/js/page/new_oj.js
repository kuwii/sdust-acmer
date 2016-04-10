$(document).ready(function() {
  $("#btn-add-new-oj").click(function() {
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
      url: "/api/oj/create/",
      async: false,
      data: data,
      dataType: "text",
      success: function(response) {
        if (response == "SUCCESS") {
          location.href = location.href = document.referrer;
        } else if (response == "OJ_EXISTS") {
          $("#div-form-group-name").addClass("has-error");
          $("#h-head").addClass("text-danger").text("OJ Exists.");
        } else {
          $("#div-form-group-name").addClass("has-error");
          $("#h-head").addClass("text-danger").text("Name Can't be empty.")
        }
      }
    });
  });
});