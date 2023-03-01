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
          alert(data.output);
        },
        error: function() {
          alert('Error running test.');
        }
      });
    });

    $('#delete-test-btn').click(function() {
      $.ajax({
        type: 'POST',
        data: {
                csrfmiddlewaretoken: csrfToken,
        },
        //headers: { "X-CSRFToken": "{{ csrf_token }}" },
        url: "/"+testId+"/delete/",
        success: function(data) {
          alert('Test deleted successfully.');
          window.location.href = "/";
        },
        error: function() {
          alert('Error deleting test.');
        }
      });
    });
});