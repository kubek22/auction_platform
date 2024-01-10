from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime
import pytz


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
@login_required
def create_auction(request, item_id):
    user = request.user
    item = Item.objects.get(seller_id=user.id, id=item_id)
    if item.on_auction:
        return redirect("my_items")
    if request.method == 'POST':
        form = AuctionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.item = item
            obj.active = True
            obj.current_price = 0
            obj.start_time = pytz.utc.localize(datetime.now())
            obj.save()
            messages.success(request, 'The auction has started.')
            # TODO FOR TOMORROW: check finishing, add current_bidder to Auction, finish started Auctions
            return redirect("my_items")
            # return render(request, 'show_item.html', {'item': item})
        else:
            messages.info(request, 'The form is not valid.')
    else:
        form = AuctionForm()

    context = {'form': form}
    return render(request, 'create_auction.html', context)


@login_required
def my_items(request):
    user = request.user
    items = Item.objects.filter(seller_id=user.id, on_auction=False)
    items_on_auctions = Item.objects.filter(seller_id=user.id, on_auction=True)
    context = {'items': items,
               'items_on_auctions': items_on_auctions}
    return render(request, 'my_items.html', context)


@login_required
def show_item(request, item_id):
    user = request.user
    item = Item.objects.get(seller_id=user.id, id=item_id)
    context = {'item': item}
    return render(request, 'show_item.html', context)
