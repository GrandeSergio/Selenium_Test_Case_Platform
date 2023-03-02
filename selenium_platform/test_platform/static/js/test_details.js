function sweetAlertConfirm(callback) {
    Swal.fire({
        title: 'Are you sure?',
        text: 'You won\'t be able to revert this!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
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
    const testId = $('tr[data-test-id]').data('test-id');
    console.log(testId)
    $('#run-test-btn').click(function() {
      $.ajax({
        type: 'POST',
        data: {
                csrfmiddlewaretoken: csrfToken,
        },
        url: "/"+testId+"/run/",
        success: function(data) {
          alert(data.result);
        },
        error: function() {
          alert('Error running test.');
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
