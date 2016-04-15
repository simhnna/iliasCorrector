$('#sync-exercises').click(function() {
  $('.overlay').removeClass('hide');
  $.ajax({
    url: "/sync",
  }).done(function() {
    setTimeout(function() {location.reload();}, 2000)
  });
});
