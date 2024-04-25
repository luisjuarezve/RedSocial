from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .modelo.credencial import Credencial
from .modelo.perfil import Perfil
from .models import DatabaseHandler
# Create your views here.


def login(request):
    return render(request, 'signup/login.html')


def signup(request):
    return render(request, 'signup/signup.html')


def signup_users(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        sname = request.POST.get('sname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        dbirth = request.POST.get('dbirth')
        relation = request.POST.get('relation')
        gender = request.POST.get('gender')
        location = request.POST.get('location')
        BDD = DatabaseHandler()
        BDD.connect()
        BDD.insertCredencial(Credencial(email, password))
        BDD.insertPerfil(Perfil(BDD.get_credencial_id(
            email, password), fname, sname, dbirth, gender, location, relation, "media/avatar-perfil.png", "media/portada.jpg"))
        BDD.close()
        messages.success(request, 'Registro Exitoso!')
        return redirect('login')
    else:
        return HttpResponse('Método no permitido')


def check_email(request):
    email = request.GET.get('email', None)
    BDD = DatabaseHandler()
    BDD.connect()
    credencial = BDD.auth_email(email)
    BDD.close()
    data = {
        'is_taken': credencial is not None
    }
    return JsonResponse(data)


def check_age(request):
    fbirth = request.GET.get('dbirth', None)
    try:
        fecha_nac = datetime.strptime(fbirth, "%Y-%m-%d")
        hoy = datetime.today()
        edad = hoy.year - fecha_nac.year - \
            ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
        if edad >= 13:
            return JsonResponse({'is_taken': False})
        else:
            return JsonResponse({'is_taken': True})
    except ValueError:
        return JsonResponse({'is_taken': False})
