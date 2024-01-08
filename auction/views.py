from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from auction.forms import ItemForm, AuctionForm
from auction.models import Item


# Create your views here.

@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.seller = request.user
            obj.save()
            messages.success(request, 'The item has been added to your account.')
        else:
            messages.info(request, 'The form is not valid.')
            print(form.errors)
    else:
        form = ItemForm()

    context = {'form': form}

    return render(request, 'add_item.html', context)

# TODO creating an auction from chosen item
# @login_required
# def create_auction(request):
#     if request.method == 'POST':
#         form = AuctionForm(request.POST)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.item =


@login_required
def my_items(request):
    user = request.user
    items = Item.objects.get(seller_id=user.id)
