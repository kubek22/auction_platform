from django.shortcuts import render

from auction.models import Auction

MAX_AUCTIONS = 10


def home(request):
    auctions = Auction.objects.filter(active=True)[:MAX_AUCTIONS]  # .order_by('?')
    context = {'auctions': auctions}
    return render(request, 'home.html', context)
