from django.urls import path

from auction import views

urlpatterns = [
    path('add_item/', views.add_item, name='add_item'),
    path('my_items/', views.my_items, name='my_items'),
    path('my_items/<int:item_id>', views.show_item, name='my_item'),
    path('my_items/create_auction/<int:item_id>', views.create_auction, name='create_auction')
]

