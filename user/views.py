from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from user.forms import RegisterForm


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The form is valid and has been saved.')
            return HttpResponseRedirect("thanks.html")
        else:
            messages.info(request, 'The form is not valid.')
    else:
        form = RegisterForm()
        messages.info(request, 'Request type is not POST.')

    context = {
        'form': form
    }
    return render(request, 'register.html', context)