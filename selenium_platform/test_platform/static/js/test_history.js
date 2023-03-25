$(document).ready(function () {
    $(".output-btn").on("click", function () {
        var output = $(this).data("output");
        Swal.fire({
            title: "Test Output",
            html: output,
            confirmButtonText: "Close",
            width: "50%",
            padding: "1rem",
        });
    });
});