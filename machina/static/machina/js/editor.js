var MachinaMarkdownEditor = MachinaMarkdownEditor | {};

MachinaMarkdownEditor = (function() {
  var isMarkdownTextarea = function(el) {
    return (' ' + el.className + ' ').indexOf(' machina-mde-markdown ') > -1;
  };

    ddd

  var init = function() {
    elements = document.getElementsByTagName("textarea");
    for (var i = 0; i < elements.length; ++i){
      if (isMarkdownTextarea(elements[i])) {
        var editor = new FroalaEditor(elements[i]);
      }
    }
  };

  return {
    init: function() {
      return init();
    },
  };
})();

window.onload = MachinaMarkdownEditor.init;
