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
            messages.success(request, 'New item has been added to your account.')
            return redirect('my_items')
        else:
            messages.error(request, 'The form is not valid.')
    else:
        form = ItemForm()

    context = {'form': form}
    return render(request, 'add_item.html', context)


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
            return redirect("my_items")
        else:
            messages.error(request, 'The form is not valid.')
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
    if (not auction.active) and auction.current_bidder == user:
        context['won'] = True
    return render(request, 'show_auction.html', context)


def show_auction(request, auction_id):
    user = request.user
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            auction = Auction.objects.get(id=auction_id)
            price = form.cleaned_data['price']
            bidder = user
            msg = auction.bid(price, bidder)
            if msg is None:
                messages.success(request, 'The auction has been bid.')
            else:
                messages.error(request, msg)
    else:
        form = BidForm()

    auction = Auction.objects.get(id=auction_id)
    context = {'auction': auction, 'form': form}
    if (not auction.active) and auction.current_bidder == user:
        context['won'] = True
    return render(request, 'show_auction.html', context)


# TODO !!!(NOW) 30 html tags
# TODO requirements.txt
