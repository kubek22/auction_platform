from django.urls import path, include

from user import views
from django.contrib.auth import views as django_views

from user.forms import LogInForm

urlpatterns = [
    path('register/', views.register, name='register'),
    # optional solution
    #path('', include("django.contrib.auth.urls")),
    #path('login/', django_views.LoginView.as_view(authentication_form=LogInForm), name="login")
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
]