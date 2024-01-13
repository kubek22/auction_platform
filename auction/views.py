from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime
import pytz

from auction.forms import ItemForm, AuctionForm, BidForm
from auction.models import Item, Auction


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
            return redirect('my_items')
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
            # TODO check finishing, add current_bidder to Auction, finish started Auctions
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
def show_my_item(request, item_id):
    user = request.user
    item = Item.objects.get(seller_id=user.id, id=item_id)
    context = {'item': item}
    return render(request, 'show_item.html', context)


@login_required
def my_auctions(request):
    user = request.user
    auctions = Auction.objects.select_related('item').filter(item__seller_id=user.id, active=True)
    # TODO auctions sold
    bidding_auctions = Auction.objects.filter(bidder=user, active=True)
    won_auctions = Auction.objects.filter(bidder=user, active=False)
    context = {'auctions': auctions,
               'bidding_auctions': bidding_auctions,
               'won_auctions': won_auctions,
               'mine': True}
    return render(request, 'my_auctions.html', context)


@login_required
def show_my_auction(request, auction_id):
    user = request.user
    auction = Auction.objects.select_related('item').get(id=auction_id, item__seller_id=user.id)
    context = {'auction': auction,
               'mine': True}
    return render(request, 'show_auction.html', context)


def show_auction(request, auction_id):
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            auction = Auction.objects.get(id=auction_id)
            price = form.cleaned_data['price']
            bidder = request.user
            auction.bid(price, bidder)
            messages.success(request, 'Successful bid.')
    else:
        form = BidForm()

    auction = Auction.objects.get(id=auction_id)
    context = {'auction': auction, 'form': form}
    return render(request, 'show_auction.html', context)


# TODO (TOMORROW) additional bars on main page (links to user items etc.)
# TODO implement the way of showing auction (seller_info, time, current_bidder, current_bid), bid logics
# TODO create my_auctions template
# TODO create template to show auctions on the main page
