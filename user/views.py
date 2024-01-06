from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from user.forms import RegisterForm, LogInForm


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The form is valid and has been saved.')
            return HttpResponseRedirect("thanks/")
        else:
            messages.info(request, 'The form is not valid.')
            # TODO
            # give accurate information when username or email is not unique
    else:
        form = RegisterForm()
        messages.info(request, 'Request type is not POST.')

    context = {
        'form': form
    }
    return render(request, 'register.html', context)


def thanks(request):
    return render(request, 'thanks.html')


def login_user(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in')
                # TODO
                # success login
            else:
                messages.info(request, 'Not logged in')
                # TODO
                # logging in not successful
        else:
            messages.info(request, 'The form is not valid')
    else:
        form = LogInForm()

    context = {'form': form}

    return render(request, 'registration/login.html', context)


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
