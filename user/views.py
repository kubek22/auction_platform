from django.contrib import messages
from django.shortcuts import render
from user.forms import RegisterForm


# Create your views here.

def register(request):
    if request.POST == 'POST':
        form = RegisterForm()
        if form.is_valid():
            form.save()
    else:
        form = RegisterForm()

    context = {
        'form': form
    }
    return render(request, 'register.html', context)