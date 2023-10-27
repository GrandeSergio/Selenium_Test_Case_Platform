function get_token() {
    return $('input[name="csrfmiddlewaretoken"]').val();
}
function sweetAlertConfirm(callback) {
    Swal.fire({
        title: 'Are you sure?',
        text: 'You won\'t be able to revert this!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!',
        darkMode: true
    }).then((result) => {
        if (result.isConfirmed) {
            callback().then((response) => {
                if (response.success) {
                    Swal.fire(
                        'Deleted!',
                        'The test has been deleted.',
                        'success'
                    ).then(() => {
                        window.location.href = "/";
                    });
                } else {
                    Swal.fire(
                        'Error!',
                        response.error_message,
                        'error'
                    );
                }
            });
        }
    });
}

$(document).ready(function() {
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    $('#run-test-btn').click(function() {
        const testId = $(this).data('test-id');
        const runUrl = $(this).data('run-url');
        const toastMessage = $('#toast-message'); // Get the toast message div

        // Perform AJAX request without the SweetAlert2 popup
        $.ajax({
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrfToken,
            },
            url: runUrl,
            success: function(data) {
                // Check if the test ran successfully
                if (data.output === 'Test passed') {
                    // Show a success toast message
                    toastMessage.text('Test ran successfully');
                    toastMessage.removeClass('error-toast').addClass('success-toast');
                } else {
                    // Show an error toast message
                    toastMessage.text('Test failed');
                    toastMessage.removeClass('success-toast').addClass('error-toast');
                }

                // Display the toast message for a few seconds
                toastMessage.fadeIn(400).delay(3000).fadeOut(400);
            },
            error: function() {
                // Show an error toast message for AJAX request failure
                toastMessage.text('Error running the test. Please try again.');
                toastMessage.removeClass('success-toast').addClass('error-toast');
                toastMessage.fadeIn(400).delay(3000).fadeOut(400);
            }
        });
    });



    $('#delete-test-btn').click(function() {
        const testId = $(this).data('test-id'); // Retrieve the test ID from the data attribute
        const deleteUrl = $(this).data('delete-url');

        sweetAlertConfirm(function() {
            return $.ajax({
                type: 'POST',
                data: {
                    csrfmiddlewaretoken: csrfToken,
                },
                url: deleteUrl,
                success: function(response) {
                    if (response.success) {
                        // Test deletion was successful, redirect to the test list page
                        Swal.fire({
                            title: 'Deleted!',
                            text: 'The test has been deleted.',
                            icon: 'success',
                            confirmButtonText: 'OK',
                            onClose: function() {
                                window.location.href = "/";
                            }
                        });
                    } else {
                        // Test deletion failed, show an error message
                        Swal.fire('Error!', response.error_message, 'error');
                    }
                },
                error: function() {
                    // An error occurred during the request
                    Swal.fire('Error!', 'Error deleting test.', 'error');
                }
            });
        }, 'The test has been deleted.', '/');
    });

});

// Add click event listener to toggle button
document.querySelectorAll('.output-toggle-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
        // Get the output container element
        var container = this.nextElementSibling;
        // Toggle the display style of the output container
        if (container.style.display === 'none') {
            container.style.display = 'block';
        } else {
            container.style.display = 'none';
        }
    });
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});


document.querySelector('[name="replace-file"]').addEventListener('click', function() {
    showReplaceModal();
});

function showReplaceModal() {
    const testId = $('tr[data-test-id]:first').data('test-id');
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const replaceFileUrl = document.querySelector('#replace-file-btn').dataset.url;

    Swal.fire({
        title: 'Replace File',
        html: `
            <form method="post" enctype="multipart/form-data" action="${replaceFileUrl}">
                <div class="form-group">
                    <label for="file">New File:</label>
                    <input type="file" class="form-control-file" id="file" name="file">
                </div>
            </form>`,
        showCancelButton: true,
        confirmButtonText: 'Replace',
        cancelButtonText: 'Close',
        preConfirm: () => {
            const fileInput = Swal.getPopup().querySelector('#file');
            const file = fileInput.files[0];

            if (file) {
                const formData = new FormData();
                formData.append('file', file);
                formData.append('csrfmiddlewaretoken', csrfToken);

                return fetch(replaceFileUrl, {
                    method: 'POST',
                    body: formData,
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(response.statusText);
                    }
                    return response.json();  // Parse the JSON response
                })
                .then(data => {
                    if (!data.success) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Oops...',
                            text: data.error  // Show the specific error message received from Django
                        });
                        throw new Error(data.error);  // Throw an error with the error message from Django
                    }
                })
            }

            return null;
        },
    })
    .then(result => {
        if (result.isConfirmed) {
            Swal.fire('File replaced successfully!');
            // Optional: Perform any additional actions after successful replacement
        }
    });
}




