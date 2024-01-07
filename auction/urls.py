from django.urls import path

from auction import views

urlpatterns = [
    path('add_item/', views.add_item, name='add_item')
]