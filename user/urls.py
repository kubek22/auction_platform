from django.urls import path, include

from user import views
from django.contrib.auth import views as django_views

from user.forms import LogInForm

urlpatterns = [
    path('register/', views.register, name='home'),
    path('register/thanks/', views.thanks, name='thx'),
    path('', include("django.contrib.auth.urls")),
    #path('login/', django_views.LoginView.as_view(authentication_form=LogInForm), name="login")
    path('login/', views.login_user, name='login')
]