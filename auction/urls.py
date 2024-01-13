from django.urls import path

from auction import views

urlpatterns = [
    path('add_item/', views.add_item, name='add_item'),
    path('my_items/', views.my_items, name='my_items'),
    path('my_items/<int:item_id>', views.show_my_item, name='my_item'),
    path('my_items/create_auction/<int:item_id>', views.create_auction, name='create_auction'),
    path('my_auctions/', views.my_auctions, name='my_auctions'),
    path('my_auctions/<int:auction_id>', views.show_my_auction, name='my_auction'),
    path('<int:auction_id>', views.show_auction, name='auction')
]

