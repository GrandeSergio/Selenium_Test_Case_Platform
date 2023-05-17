$(document).ready(function(){
    var isFormVisible = false;
    $("#form").hide();
    $("#edit-btn").click(function(){
        if (isFormVisible) {
            $(".code-text").show();
            $("#form").hide();
            $("#edit-btn").text("Edit");
            isFormVisible = false;
        } else {
            $(".code-text").hide();
            $("#form").show();
            $("#edit-btn").text("Save");
            isFormVisible = true;
        }
    });
    $("#form").submit(function() {
        // Submit the form and prevent the default form submission behavior
        $.post($(this).attr("action"), $(this).serialize(), function(data) {
            $(".code-text").text(data);
            $(".code-text").show();
            $("#form").hide();
            $("#edit-btn").text("Edit");
            isFormVisible = false;
        });
        return false;
    });
    $("#save-btn").click(function() {
        $("#form").submit();
    });
});
