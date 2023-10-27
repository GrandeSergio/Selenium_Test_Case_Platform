$(document).ready(function() {
  $('#upload_button').click(function(event) {
    event.preventDefault();
    var form = $('form')[0];
    var formData = new FormData(form);
    $.ajax({
      type: 'POST',
      url: upload_url,
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        if (response.success) {
          Swal.fire({
            icon: 'success',
            title: 'File uploaded successfully!',
            showConfirmButton: true,
            confirmButtonText: 'Go To Uploaded Test Case',
            showCancelButton: true,
            cancelButtonText: 'Upload Next Test Case',
          }).then(function(result) {
            if (result.isConfirmed) {
              window.location.href = response.test_case_url;
            } else {
              $('#name').val('');
              $('#file').val('');
            }
          });
        } else {
          Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: response.error  // Show the error message received from Django
          });
        }
      },
      error: function(xhr, status, error) {
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'An error occurred. Please try again later.'
        });
      }
    });
  });
});
