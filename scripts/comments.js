function leaveComment() {
  // Here, "this" is the button that the user clicked.
  var button = $(this);

  // Move through the DOM tree to find the "likes"
  // element that corresponds to the clicked button.

  // Look through parents of this to find .photo.
  var post = $(this).parents('.post');

  // Look inside photo to find .likes.
  var comments = $(post).find('.comments');

  // Get the URLsafe key from the button value.
  var urlsafeKey = $(button).val();

  // Send a POST request and handle the response.
  $.post('/new_comment', {'post_key': urlsafeKey}, function(response) {
    // Update the number in the "like" element.
    $(comments).text(response);
  });
}

$('.post button').click(leaveComment);
