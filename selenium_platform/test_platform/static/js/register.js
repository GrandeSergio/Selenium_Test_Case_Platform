
$(document).ready(function() {
  if (typeof toastRegisterMessages !== 'undefined' && toastRegisterMessages.length > 0) {
    var toastHTML = '<div class="toast align-items-center text-white bg-danger border-0 animated-toast" role="alert" aria-live="assertive" aria-atomic="true">' +
      '<div class="d-flex">' +
        '<div class="toast-body">' +
          '<ul class="mb-0">';
    
    toastRegisterMessages.forEach(function(message) {
      toastHTML += '<li>' + message + '</li>';
    });
    
    toastHTML += '</ul></div>' +
      '<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>' +
      '</div>' +
      '</div>';
    
    var toastContainer = $(toastHTML);
    $('body').append(toastContainer);
    toastContainer.toast('show');
  }
});
