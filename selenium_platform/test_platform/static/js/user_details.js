// Add event listener to the delete account button
document.getElementById('delete-account-btn').addEventListener('click', function() {
  // Show SweetAlert2 confirmation dialog
  Swal.fire({
    title: 'Delete Account',
    text: 'Are you sure you want to delete your account?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: 'Delete',
    cancelButtonText: 'Cancel'
  }).then((result) => {
    // If user confirms deletion, submit the form
    if (result.isConfirmed) {
      document.getElementById('delete-account-form').submit();
    }
  });
});

window.addEventListener('DOMContentLoaded', function() {
    var containerHeight = document.querySelector('.main-container').offsetHeight;
    document.getElementById('custom-row').style.height = containerHeight + 'px';
});