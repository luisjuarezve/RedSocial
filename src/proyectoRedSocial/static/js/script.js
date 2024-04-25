$(document).ready(function () {
    // Validar el correo electronico
    $('#email').change(function () {
        var email = $(this).val();
        $.ajax({
            url: 'signup/check_email',
            data: {
                'email': email
            },
            dataType: 'json',
            success: function (data) {
                if (data.is_taken) {
                    $('#email').addClass('is-invalid');
                    $('#email').attr('title', 'Correo registrado en la base de datos');
                    $('#error-message-email').text('Este correo ya está registrado en la base de datos');
                    $('#error-message-email').addClass('alert alert-danger');
                    $('#registrar').prop('disabled', true);
                } else {
                    $('#email').removeClass('is-invalid');
                    $('#email').addClass('is-valid');
                    $('#email').removeAttr('title');
                    $('#error-message-email').text('');
                    $('#error-message-email').removeClass('alert alert-danger');
                    $('#registrar').prop('disabled', false);
                }
            }
        });
    });

    // Validar la edad mínima (debe tener al menos 13 años)
    $('#dbirth').change(function () {
        var dbirth = $(this).val();
        $.ajax({
            url: 'signup/check_age',
            data: {
                'dbirth': dbirth
            },
            dataType: 'json',
            success: function (data) {
                if (data.is_taken) {
                    $('#dbirth').addClass('is-invalid');
                    $('#dbirth').attr('title', 'Tienes que tener al menos 13 años para registrarte');
                    $('#error-message-dbirth').text('Tienes que tener al menos 13 años para registrarte');
                    $('#error-message-dbirth').addClass('alert alert-danger');
                    $('#registrar').prop('disabled', true);
                } else {
                    $('#dbirth').removeClass('is-invalid');
                    $('#dbirth').addClass('is-valid');
                    $('#dbirth').removeAttr('title');
                    $('#error-message-dbirth').text('');
                    $('#error-message-dbirth').removeClass('alert alert-danger');
                    $('#registrar').prop('disabled', false);
                }
            }
        });
    });

});
