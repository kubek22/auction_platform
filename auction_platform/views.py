from django.shortcuts import render

from auction.models import Auction


def home(request):
    auctions = Auction.objects.filter(active=True)
    context = {'auctions': auctions}
    return render(request, 'home.html', context)
