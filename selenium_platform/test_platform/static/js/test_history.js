$('.output-btn').on('click', function() {
    var output = $(this).data('output');
    var run_id = $(this).data('run-id');
    var url = '/run_output/' + run_id + '/';
    $('#test-history-container').load(url);
});

$('#run-test-btn').on('click', function() {
    var test_id = $('#test-details-container').data('test-id');
    var url = '{% url "run_test_cases" test_id=test_id %}';
    $.post(url, {csrfmiddlewaretoken: get_token()}, function(data) {
        var run_id = data.run_id;
        var url = '/run_output/' + run_id + '/';
        $('#test-history-container').load(url);
    });
});
