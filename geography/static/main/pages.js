$(document).ready(function(){
  $('[data-toggle="popover"]').popover();
  $("#name").click(function() {
    $.ajax({
      url: "{% if public == 'public' %} {% url 'projects' public 'title' page_num %} {% else %} {% url 'projects' public.id 'title' page_num %} {% endif %}", 
      success: function(result) {
          $('#projects').replaceWith(result);
      }});
    });
  });

  $("#next").click(function() {
    $.ajax({
      url: "{% if public == 'public' %} {% url 'projects' public sort page_num|add:'1' %} {% else %} {% url 'projects' public.id sort page_num|add:'1' %} {% endif %}",
      success: function(result) {
          $('#projects').replaceWith(result);
    }});
  });

  $("#prev").click(function() {
    $.ajax({
      url: "{% if public == 'public' %} {% url 'projects' public sort page_num|add:'-1' %} {% else %} {% url 'projects' public.id sort page_num|add:'-1' %} {% endif %}",
      success: function(result) {
          $('#projects').replaceWith(result);
    }});
  });