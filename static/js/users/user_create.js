$(document).ready(function () {
    $('#user-create-form').on('submit', function (e) {
        e.preventDefault();

        let form = $(this)[0];
        let formData = new FormData(form);
        var url = $(this).attr('data-url');

        $.ajax({
            url: url,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.success) {
                    alertSwitch('success', response.message);
                    form.reset();
                } else {
                    alertSwitch('error', "Error: " + response.message);
                }
            },
            error: function (xhr, status, error) {
                console.error("Error:", error);
                alertSwitch('error', "Error al procesar la solicitud.");
            }
        });
    });
});
