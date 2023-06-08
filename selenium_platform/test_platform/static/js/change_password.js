$(document).ready(function() {
  var toastHTML = '';
  if (typeof toastMessages !== 'undefined') {
    toastMessages.forEach(function(messageObj) {
      var message = messageObj.message;
      var type = messageObj.type;

      var toastClass = 'bg-primary';
      if (type === 'error') {
        toastClass = 'bg-danger';
      } else if (type === 'success') {
        toastClass = 'bg-success';
      }

      toastHTML += '<div class="toast align-items-center text-white border-0 animated-toast ' + toastClass + '" role="alert" aria-live="assertive" aria-atomic="true">' +
        '<div class="d-flex">' +
          '<div class="toast-body">' +
            message +
          '</div>' +
          '<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>' +
        '</div>' +
      '</div>';
    });
  }
  var toastContainer = $(toastHTML);
  $('body').append(toastContainer);
  toastContainer.toast('show');
});