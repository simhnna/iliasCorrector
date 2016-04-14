$('#sync-exercises').click(function() {
  $('.overlay').removeClass('hide');
  $.ajax({
    url: "/sync",
  }).done(function() {
    setTimeout(function() {location.reload();}, 2000)
  });
});

$('#import-grades').click(function() {
  $('.overlay').removeClass('hide');
});
