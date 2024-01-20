from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from user.forms import RegisterForm, LogInForm, ForgotPasswordForm
from user.models import User


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The user has been created.')
            username = form.cleaned_data["username"]
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'The form is not valid.')
    else:
        form = RegisterForm()

    context = {
        'form': form
    }
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in')
                return redirect('home')
            else:
                messages.error(request, 'Not logged in')
        else:
            messages.error(request, 'The form is not valid')
    else:
        form = LogInForm()

    context = {'form': form}

    return render(request, 'registration/login.html', context)


# alternative version (not used)
def userLoginPage(request):
    form = LogInForm(request.POST)

    context = {
        'form': form
    }

    print('www')

    if request.method == 'POST':
        # form = UserLoginForm(request.POST)
        print('post')

        print(form.is_valid())
        print(form.base_fields)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            print(user)
            # print(request.user.is_authenticated())
            if user is not None:
                # print(request.user.is_authenticated())
                print('login')
                login(request, user)
                # Redirect to a success page.
                # context['form'] = UserLoginForm()
            else:
                print("Error")

    print('render')

    return render(request, 'registration/login.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out user.")
    return redirect('home')


def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            # code for sending an email
            print('Sending an email...')
            messages.success(request, 'The email has been sent.')
        else:
            messages.error(request, 'No user with given email.')
    else:
        form = ForgotPasswordForm()

    context = {'form': form}
    return render(request, 'forgot_password.html', context)
