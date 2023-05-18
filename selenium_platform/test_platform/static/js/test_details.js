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

/*$(document).ready(function() {
    // Disable the Run Test button after it has been clicked
   $('#run-test-btn').on('click', function() {
      $(this).prop('disabled', true);
    });
});*/

$(document).ready(function() {
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    const testId = $('tr[data-test-id]:first').data('test-id');
    console.log('test ', testId)

    $('#run-test-btn').click(function() {
        // Display sweetalert2 popup with options
        Swal.fire({
            title: 'Choose running mode',
            showCancelButton: true,
            confirmButtonText: 'Batch mode',
            cancelButtonText: 'Foreground mode',
            reverseButtons: true,
            icon: 'info',
            darkMode: true
        }).then((result) => {
            if (result.isConfirmed) {
                // User selected batch mode
                $.ajax({
                    type: 'POST',
                    data: {
                        csrfmiddlewaretoken: csrfToken,
                        mode: 'batch'
                    },
                    url: "/"+testId+"/run/",
                    success: function(data) {
                        alert(data.result);
                    },
                    error: function() {
                        alert('Error running test.');
                    }
                });
            } else if (result.dismiss === Swal.DismissReason.cancel) {
                // User selected foreground mode
                $.ajax({
                    type: 'POST',
                    data: {
                        csrfmiddlewaretoken: csrfToken,
                        mode: 'foreground'
                    },
                    url: "/"+testId+"/run/",
                    success: function(data) {
                        alert(data.result);
                    },
                    error: function() {
                        alert('Error running test.');
                    }
                });
            }
        });
    });

    $('#delete-test-btn').click(function() {
        sweetAlertConfirm(function() {
            return $.ajax({
                type: 'POST',
                data: {
                    csrfmiddlewaretoken: csrfToken,
                },
                url: "/"+testId+"/delete/",
                success: function(data) {
                    //alert('Test deleted successfully.');
                },
                error: function() {
                    //alert('Error deleting test.');
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
    Swal.fire({
        title: 'Replace File',
        html: `
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                <div class="form-group">
                    <label for="file">File:</label>
                    <input type="file" class="form-control-file" id="file" name="file">
                </div>
            </form>`,
        showCancelButton: true,
        confirmButtonText: 'Upload',
        cancelButtonText: 'Close',
        preConfirm: () => {
            const fileInput = Swal.getPopup().querySelector('#file');
            const file = fileInput.files[0];

            if (file) {
                const formData = new FormData();
                formData.append('file', file);

                return fetch('/upload', {
                    method: 'POST',
                    body: formData,
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(response.statusText);
                    }
                })
                .catch(error => {
                    Swal.showValidationMessage(`Request failed: ${error}`);
                });
            }

            return null;
        },
    })
    .then(result => {
        if (result.isConfirmed) {
            Swal.fire('File uploaded successfully!');
            // Additional actions after successful upload
        }
    });
}




