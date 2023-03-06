$(document).ready(function() {
  $('#upload_button').click(function(event) {
    event.preventDefault();
    var form = $('form')[0];
    var formData = new FormData(form);
    $.ajax({
      type: 'POST',
      url: custom_upload_url,
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        if (response.success) {
          Swal.fire({
            icon: 'success',
            title: 'File uploaded successfully!',
            showConfirmButton: true, // Added option to stay on upload page or go to test details page
            confirmButtonText: 'Go To Uploaded Test Case', // Added text for confirmation button
            showCancelButton: true, // Added cancel button
            cancelButtonText: 'Upload Next Test Case', // Added text for cancel button
          }).then(function(result) {
            if (result.isConfirmed) { // If user clicked "Go to Test Details"
              window.location.href = response.test_case_url;
            } else { // If user clicked "Stay Here"
              $('#name').val(''); // Reset form values
              $('#file').val('');
            }
          });
        } else {
          Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Something went wrong!'
          });
        }
      },
      error: function(xhr, status, error) {
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Something went wrong!'
        });
      }
    });
  });
});
