function clickLike() {
  // Here, "this" is the button that the user clicked.
  var button = $(this);

  // Move through the DOM tree to find the "likes"
  // element that corresponds to the clicked button.

  // Look through parents of this to find .photo.
  var photo = $(this).parents('.photo');

  // Look inside photo to find .likes.
  var likes = $(photo).find('.likes');

  // Get the URLsafe key from the button value.
  var urlsafeKey = $(button).val();

  // Send a POST request and handle the response.
  $.post('/likes', {'photo_key': urlsafeKey}, function(response) {
    // Update the number in the "like" element.
    $(likes).text(response);
  });
}

$('.photo button').click(clickLike);
