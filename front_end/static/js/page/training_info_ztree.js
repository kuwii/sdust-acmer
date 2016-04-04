var target_username = $("#target-user").text();

var setting = {
  async: {
    enable: true,
    type: "get",
    url: "/api/categories/get-user-info/"+target_username+"/",
    dataType: "json",
    dataFilter: function(treeId, parentNode, responseData) {
      var ret = []

      var categories = responseData.categories;

      for(var i = 0; i != categories.length; ++i) {
        var num_solved = categories[i].num_solved;
        var num_tried = categories[i].num_tried;
        var num_all = categories[i].num_all;

        var per = num_solved/num_all * 100.0;
        per = per.toFixed(3);
        ret.push({
          id: categories[i].name,
          name: categories[i].caption + "  [solved/ tried/ total: "+num_solved+"/ "+num_tried+"/ "+num_all+" - "+per+"%]",
          isParent: true
        });
      }

      var problems = responseData.problems;

      var problems_solved = problems.solved;
      var problems_not_solved = problems.not_solved;
      var problems_not_tried = problems.not_tried;

      for(var i = 0; i != problems_solved.length; ++i) {
        ret.push({
          id: problems_solved[i].id,
          name: problems_solved[i].title + "   [solved]",
          isParent: false,
          font:{'color':'green'}
        });
      }
      for(var i = 0; i != problems_not_solved.length; ++i) {
        ret.push({
          id: problems_not_solved[i].id,
          name: problems_not_solved[i].title + "   [tried]",
          isParent: false,
          font:{'color':'red'}
        });
      }
      for(var i = 0; i != problems_not_tried.length; ++i) {
        ret.push({
          id: problems_not_tried[i].id,
          name: problems_not_tried[i].title + "   [not tried]",
          isParent: false,
          font:{'color':'grey'}
        });
      }


      return ret;
    },
    autoParam: ["id=name"]
  },
  view: {
    fontCss: getFont,
    nameIsHTML: true
  }
};

$(document).ready(function(){
  $.fn.zTree.init($("#category-tree"), setting);
});

function getFont(treeId, node) {
  return node.font ? node.font : {};
}