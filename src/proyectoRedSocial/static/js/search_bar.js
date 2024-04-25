$(document).ready(function () {
    $('#search_bar').on('submit', function (event) {
        event.preventDefault();
        var searchQuery = $(this).find('input[name="search_bar"]').val();
        if (searchQuery) {
            $.ajax({
                url: 'search_user', // Asegúrate de que esta URL apunta a tu función app_search_user
                type: 'GET',
                data: { search_bar: searchQuery }, // Aquí pasamos la query del usuario
                success: function (data) {
                    $('#results').empty();
                    if (data.length > 0) {
                        $('.lista').show(); // Muestra el div
                        data.forEach(function (user) {
                            $('#results').append('<li><a class="border-bottom p-2 text-decoration-none d-flex gap-2" href="/app/perfil/id/' + user.id + '"><img src="' + user.foto_perfil + '" alt="mdo" width="32" height="32" class="rounded-circle">' + user.nombre + ' ' + user.apellido + '</img></a></li>');
                        });
                    } else {
                        $('.lista').hide(); // Oculta el div
                    }
                }
            });
        } else {
            $('#results').empty();
            $('.lista').hide(); // Oculta el div
        }
    });


    $('#Actualizarfoto').click(function () {
        $('#fotoperfil').click();

    });

    $('#fotoperfil').change(function () {
        if (this.value) {
            $('#myForm').submit();
        }
    });

    //Codigo actualizar foto perfil
    $('#Actualizarfotoperfil').click(function () {
        $('#overlay_foto_perfil').show();
    });

    $('#overlay_foto_perfil').click(function (event) {
        if (event.target == this) {
            $(this).hide();
        }
    });
    //Codigo actualizar foto Portada
    $('#Actualizarfotoportada').click(function () {
        $('#overlay_foto_portada').show();
    });

    $('#overlay_foto_portada').click(function (event) {
        if (event.target == this) {
            $(this).hide();
        }
    });

});
