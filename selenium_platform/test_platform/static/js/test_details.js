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
    // Disable the Run Test button after it has been clicked
   $('#run-test-btn').on('click', function() {
      $(this).prop('disabled', true);
    });
});

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
/*$('#run-test-btn').on('click', function() {
    var test_id = $('#test-details-container').data('test-id');
    var url = '{% url "run_test_cases" test_id=test_id %}';
    $.post(url, {csrfmiddlewaretoken: get_token()}, function(data) {
        var run_id = data.run_id;
        var url = '/run_output/' + run_id + '/';
        $('#test-history-container').load(url);
    });
});*/

