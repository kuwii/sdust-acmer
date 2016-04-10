$(document).ready(function() {
  $("#btn-create-new-group").click(function() {
    var name = $("#input-group-name").val();
    var caption = $("#input-group-caption").val();
    var public = $("input[name='radio-group-public']:checked").val();
    var introduction = $("#input-group-introduction").val();

    if (name == "") {
        $("#btn-create-new-group").removeClass("btn-primary").addClass("btn-danger").text("Name is necessary field.");
    } else if (caption == "") {
        $("#btn-create-new-group").removeClass("btn-primary").addClass("btn-danger").text("Caption is necessary field.");
    } else {
      $.ajax({
        type: "POST",
        url: "/api/group/create/",
        async: false,
        data: {
          "name": name,
          "caption": caption,
          "public": public,
          "introduction": introduction
        },
        dataType: "text",
        success: function(response) {
          if (response == "SUCCESS") {
              $("#btn-create-new-group").removeClass("btn-primary").removeClass("btn-danger").addClass("btn-success disabled").text("Created");
          } else {
              $("#btn-create-new-group").removeClass("btn-primary").addClass("btn-danger").text(response);
          }
        }
      });
    }
  });
});