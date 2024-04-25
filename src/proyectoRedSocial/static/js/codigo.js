$(document).ready(function () {
    $('#results_solicitudes').hide();
    $('#mostrarSolicitudes').click(function () {
        var listaSolicitudes = $('#results_solicitudes');
        if (listaSolicitudes.is(":visible")) {
            // Si la lista ya está visible, la ocultamos
            listaSolicitudes.hide();
        } else {
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            const csrftoken = getCookie('csrftoken');
            // Si la lista está oculta, hacemos la petición AJAX y la mostramos
            $.ajax({
                url: 'search_request',  // Cambia esto por la ruta a tu endpoint
                type: 'GET',
                success: function (data) {
                    listaSolicitudes.empty();  // Limpiamos la lista antes de añadir las nuevas solicitudes
                    if (data.length > 0) {  // Solo mostramos la lista si hay datos
                        data.forEach(function (solicitud) {
                            listaSolicitudes.append('<li class="d-flex flex-row"><div class="border-bottom p-2 text-decoration-none" href="/app/perfil/id/' + solicitud.id + '"><div class="d-flex gap-2"><img src="' + solicitud.foto_perfil + '" alt="mdo" width="32" height="32" class="rounded-circle"></img>' + solicitud.nombre + ' ' + solicitud.apellido + '</div><p class="p-2">Te envio una solicitud de amistad: ' + solicitud.fecha + '</p><div class="d-flex gap-2"><button class="btn btn-primary" id="btn-aceptar-' + solicitud.id + '">Aceptar</button><button class="btn btn-danger" id="btn-rechazar-' + solicitud.id + '">Rechazar</button></div></div></div></li>');

                            // Agregamos el evento de clic para el botón de aceptar
                            $('#btn-aceptar-' + solicitud.id).click(function () {
                                $.ajax({
                                    url: 'auth/insert/amigo/' + solicitud.id + '',  // Cambia esto por la ruta a tu endpoint
                                    type: 'POST',
                                    data: { id: solicitud.id, csrfmiddlewaretoken: csrftoken },
                                    success: function (data) {
                                        $('#results_solicitudes').hide();
                                        alert('Solicitud aceptada');
                                    },
                                    error: function (error) {
                                        console.log(error);
                                    }
                                });
                            });

                            // Agregamos el evento de clic para el botón de rechazar
                            $('#btn-rechazar-' + solicitud.id).click(function () {
                                $.ajax({
                                    url: 'auth/drop/request/' + solicitud.id + '',  // Cambia esto por la ruta a tu endpoint
                                    type: 'POST',
                                    data: { id: solicitud.id, csrfmiddlewaretoken: csrftoken },
                                    success: function (data) {
                                        $('#results_solicitudes').hide();
                                        alert('Solicitud rechazada');
                                    },
                                    error: function (error) {
                                        console.log(error);
                                    }
                                });
                            });
                        });
                        listaSolicitudes.show();  // Mostramos la lista de solicitudes
                    } else {
                        alert('No hay Solicitudes de amistad')
                    }
                },
                error: function (error) {
                    console.log(error);
                }
            });

        }
    });

    $("#delete_friend").hover(function () {
        $(this).text("Eliminar Amigo");
        $(this).toggleClass("btn-primary btn-danger");
    }, function () {
        $(this).text("Es amigo");
        $(this).toggleClass("btn-danger btn-primary");
    });
    //codigo actualizar datos
    $('#btn_actualizar').click(function () {
        $('#overlay').show();
    });

    $('#overlay').click(function (event) {
        if (event.target == this) {
            $(this).hide();
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
