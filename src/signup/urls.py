from django.urls import path
from signup import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('signup/users', views.signup_users, name='signup_users'),
    path('signup/check_email', views.check_email, name='check_email'),
    path('signup/check_age', views.check_age, name='check_age'),
]
