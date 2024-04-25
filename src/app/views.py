from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.urls import reverse
from django.conf import settings
from .models import DatabaseHandler
from .modelo.credencial import Credencial
from .modelo.publicacion import Publicacion
from .modelo.solicitudes import Solicitud
from .modelo.comentarios import Comentario
from datetime import datetime
from .modelo.likes import Like
from .modelo.amigos import Amigo
# Create your views here.


def login_required_custom(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if 'perfil_id' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return _wrapped_view_func


@login_required_custom
def perfil(request):
    if 'perfil_id' not in request.session:
        return redirect('login')
    return render(request, 'app/perfil.html')


def app_auth(request):
    if request.method == 'POST':
        correo = request.POST['correo_electronico']
        contrasena = request.POST['contrasena']
        # Consulta SQL personalizada para verificar las credenciales
        BDD = DatabaseHandler()
        BDD.connect()
        row = BDD.get_credencial_id(Credencial(correo, contrasena))
        if row:
            credencial_id = row[0]
            perfil = BDD.get_perfil_by_credencial(credencial_id)
            request.session['perfil_id'] = perfil[0][0]
            request.session.save()
            return redirect('inicio')  # Redirige a la página de perfil
        else:
            return redirect('login')
        BDD.close()
    return redirect('login')


def cerrar_sesion(request):
    del request.session['perfil_id']
    return redirect('login')


def app_insert_amigo(request, perfil_id_request):
    if request.method == 'POST':
        perfil_id = request.session['perfil_id']
        BDD = DatabaseHandler()
        BDD.connect()
        BDD.insertAmigo(Amigo(perfil_id, perfil_id_request))
        BDD.close()
    return redirect(reverse('perfil_id', args=[perfil_id_request]))


def app_drop_amigo(request, perfil_id_request):
    if request.method == 'POST':
        perfil_id = request.session['perfil_id']
        BDD = DatabaseHandler()
        BDD.connect()
        BDD.drop_amigo(Amigo(perfil_id, perfil_id_request))
        BDD.close()
    return redirect(reverse('perfil_id', args=[perfil_id_request]))


def app_send_request(request, perfil_id_request):
    if request.method == 'POST':
        perfil_id = request.session['perfil_id']
        BDD = DatabaseHandler()
        BDD.connect()
        exist = BDD.get_solicitud(perfil_id, perfil_id_request)
        print(exist)
        if not exist:
            BDD.insertSolicitud(Solicitud(perfil_id, perfil_id_request))
            return app_perfil_id(request, perfil_id_request)
        else:
            return app_perfil_id(request, perfil_id_request)
        BDD.close()


def app_drop_request(request, perfil_id_request):
    if request.method == 'POST':
        perfil_id = request.session['perfil_id']
        BDD = DatabaseHandler()
        BDD.connect()
        BDD.drop_solicitud(Solicitud(perfil_id_request, perfil_id))
        BDD.close()
        return redirect(reverse("perfil_id", args=[perfil_id_request]))
    return HttpResponse("Solicitud eliminada Exitosamente.")


def app_cancel_request(request, perfil_id_request):
    if request.method == 'POST':
        perfil_id = request.session['perfil_id']
        BDD = DatabaseHandler()
        BDD.connect()
        BDD.drop_solicitud(Solicitud(perfil_id, perfil_id_request))
        BDD.close()
        return redirect(reverse("perfil_id", args=[perfil_id_request]))
    return HttpResponse("Solicitud cancelada Exitosamente.")


def app_send_post(request):
    if request.method == 'POST':
        perfil_id = request.session['perfil_id']
        contenido = request.POST['contenido']
        BDD = DatabaseHandler()
        BDD.connect()
        if request.FILES.get('imagen'):
            # Obtener el archivo de imagen del formulario
            imagen = request.FILES['imagen']
            # Guardar la imagen en la carpeta media
            url_img = path = default_storage.save(
                f'media/{imagen.name}', ContentFile(imagen.read()))
        else:
            url_img = ""
        BDD.insertPublicacion(Publicacion(contenido, perfil_id, url_img))
        BDD.close()
        next_url = request.POST.get('next', 'inicio')
        return redirect(next_url)
    return HttpResponse("Error al cargar la publicación.")


def app_delete_post(request, publicacion_id):
    if request.method == 'POST':
        perfil_id = request.session['perfil_id']
        BDD = DatabaseHandler()
        BDD.connect()
        BDD.drop_publicacion(perfil_id, publicacion_id)
        BDD.close()
        next_url = request.POST.get('next', 'inicio')
    return redirect(next_url)


def app_update_foto(request):
    if request.method == 'POST':
        perfil_id = request.session['perfil_id']
        BDD = DatabaseHandler()
        BDD.connect()
        if request.FILES.get('imagen'):
            # Obtener el archivo de imagen del formulario
            imagen = request.FILES['imagen']
            # Guardar la imagen en la carpeta media
            url_img = path = default_storage.save(
                f'media/{imagen.name}', ContentFile(imagen.read()))
            BDD.update_foto_perfil(perfil_id, url_img)
            BDD.close()
        else:
            url_img = ""
        return redirect("perfil")
    return HttpResponse("Foto cargada")


def app_update_foto_portada(request):
    if request.method == 'POST':
        perfil_id = request.session['perfil_id']
        BDD = DatabaseHandler()
        BDD.connect()
        if request.FILES.get('imagen'):
            # Obtener el archivo de imagen del formulario
            imagen = request.FILES['imagen']
            # Guardar la imagen en la carpeta media
            url_img = path = default_storage.save(
                f'media/{imagen.name}', ContentFile(imagen.read()))
            BDD.update_foto_portada(perfil_id, url_img)
            BDD.close()
        else:
            url_img = ""
        return redirect("perfil")
    return HttpResponse("Foto cargada")


def app_update_perfil(request):
    if request.method == 'POST':
        perfil_id = request.session['perfil_id']
        BDD = DatabaseHandler()
        BDD.connect()
        BDD.update_perfil(perfil_id, request.POST['fname'], request.POST['sname'], request.POST['dbirth'],
                          request.POST['gender'], request.POST['relation'], request.POST['location'])
        BDD.close()
        return redirect("perfil")
    return HttpResponse("Perfil Actualizado Exitosamente")


def app_send_comment(request):
    if request.method == 'POST':
        perfil_id = request.session["perfil_id"]
        contenido = request.POST['post_comments']
        BDD = DatabaseHandler()
        BDD.connect()
        id_postss = request.POST['id_post']
        BDD.insertComentario(Comentario(contenido, id_postss, perfil_id))
        BDD.close()
        next_url = request.POST.get('next', 'inicio')
        return redirect(next_url)
    return HttpResponse("Error al enviar el comentario.")


def app_update_like(request):
    if request.method == 'POST':
        perfil_id = request.session["perfil_id"]
        id_postss = request.POST['id_post']
        BDD = DatabaseHandler()
        BDD.connect()
        exist = BDD.get_like(Like(id_postss, perfil_id))
        if exist == []:
            BDD.insertLike(Like(id_postss, perfil_id))
        else:
            BDD.drop_like(Like(id_postss, perfil_id))
        BDD.close()
        next_url = request.POST.get('next', 'inicio')
        return redirect(next_url)
    return HttpResponse("Error: Método no permitido.")


def app_feed(request):
    perfil_id = request.session['perfil_id']
    post_comments = []
    all_post = []
    all_status_likes = []
    BDD = DatabaseHandler()
    BDD.connect()
    perfil = BDD.get_perfil(perfil_id)
    all_perfil = BDD.get_all_amigos(perfil_id)
    all_perfil.extend(perfil)
    for p in all_perfil:
        posts = BDD.get_all_publicacion(p[0])
        if posts:
            for post in posts:
                all_post.append(post)
                likes = BDD.get_like(Like(post[0], perfil_id))
                if likes:
                    for like in likes:
                        all_status_likes.append(like)
                else:
                    lista = (post[0], False)
                    all_status_likes.append(lista)
                comments = BDD.get_all_comentarios(post[0])
                if comments:
                    for coment in comments:
                        post_comments.append(coment)
    all_post.sort(key=lambda x: x[0], reverse=True)
    post_comments.sort(key=lambda x: x[5], reverse=False)
    BDD.close()
    return render(request, 'app/inicio.html', {'post': all_post, 'comments': post_comments, 'perfil_data': perfil, 'status_like': all_status_likes})


def app_perfil(request):
    perfil_id = request.session['perfil_id']
    post_comments = []
    all_post = []
    all_status_likes = []
    BDD = DatabaseHandler()
    BDD.connect()
    amigos = BDD.get_all_amigos(perfil_id)
    perfil = BDD.get_perfil(perfil_id)
    posts = BDD.get_all_publicacion(perfil_id)
    if posts:
        for post in posts:
            all_post.append(post)
            likes = BDD.get_like(Like(post[0], perfil_id))
            if likes:
                for like in likes:
                    all_status_likes.append(like)
            else:
                lista = (post[0], False)
                all_status_likes.append(lista)
            comments = BDD.get_all_comentarios(post[0])
            if comments:
                for coment in comments:
                    post_comments.append(coment)
    all_post.sort(key=lambda x: x[0], reverse=True)
    post_comments.sort(key=lambda x: x[5], reverse=False)
    BDD.close()
    return render(request, 'app/perfil.html', {'post': all_post, 'comments': post_comments, 'perfil_data': perfil, 'status_like': all_status_likes, 'Lista_Amigos': amigos})


def app_perfil_id(request, perfil_amigo):
    perfil_id = request.session['perfil_id']
    post_comments = []
    all_post = []
    all_status_likes = []
    BDD = DatabaseHandler()
    status = False
    solicitud_enviada = False
    BDD.connect()
    if BDD.get_amigo(perfil_id, perfil_amigo) == []:
        status_amistad = False
        if BDD.get_solicitud(perfil_amigo, perfil_id) == []:
            status = False
            if BDD.get_solicitud(perfil_id, perfil_amigo) == []:
                solicitud_enviada = False
            else:
                solicitud_enviada = True
        else:
            status = True
    else:
        status_amistad = True
    amigos = BDD.get_all_amigos(perfil_amigo)
    perfil = BDD.get_perfil(perfil_id)
    perfil_data = BDD.get_perfil(perfil_amigo)
    posts = BDD.get_all_publicacion(perfil_amigo)
    if posts:
        for post in posts:
            all_post.append(post)
            likes = BDD.get_like(Like(post[0], perfil_id))
            if likes:
                for like in likes:
                    all_status_likes.append(like)
            else:
                lista = (post[0], False)
                all_status_likes.append(lista)
            comments = BDD.get_all_comentarios(post[0])
            if comments:
                for coment in comments:
                    post_comments.append(coment)
    all_post.sort(key=lambda x: x[0], reverse=True)
    post_comments.sort(key=lambda x: x[5], reverse=False)
    BDD.close()
    if perfil_id != perfil_amigo:
        return render(request, 'app/perfil_id/perfil_friend.html', {'post': all_post, 'comments': post_comments, 'perfil_data': perfil_data, 'perfil': perfil, 'solicitud_enviada': solicitud_enviada, 'solicitud': status, 'Lista_Amigos': amigos, 'status_amistad': status_amistad})
    else:
        return redirect('inicio')


def app_search_user(request):
    if request.method == 'GET':
        perfil_id = request.session['perfil_id']
        nombre = request.GET['search_bar']
        BDD = DatabaseHandler()
        BDD.connect()
        personas = BDD.get_perfil_by_name(nombre)
        BDD.close()
        personas_json = [persona_a_json(
            persona) for persona in personas if persona[0] != perfil_id]
        return JsonResponse(personas_json, safe=False)


def app_search_request(request):
    if request.method == 'GET':
        perfil_id = request.session['perfil_id']
        BDD = DatabaseHandler()
        BDD.connect()
        solicitudes = BDD.get_all_solicitudes(perfil_id)
        BDD.close()
        solicitudes_json = [solicitud_a_json(
            solicitud) for solicitud in solicitudes]
        return JsonResponse(solicitudes_json, safe=False)


def persona_a_json(persona):
    return {
        'id': persona[0],
        'nombre': persona[1],
        'apellido': persona[2],
        'foto_perfil': settings.MEDIA_URL + persona[8],
        'foto_portada': settings.MEDIA_URL + persona[9]
    }


def solicitud_a_json(solicitud):
    fecha_formateada = solicitud[4].strftime('%d/%m/%Y a las %H:%M:%S')
    return {
        'id': solicitud[0],
        'nombre': solicitud[1],
        'apellido': solicitud[2],
        'foto_perfil': settings.MEDIA_URL + solicitud[3],
        'fecha': fecha_formateada
    }
