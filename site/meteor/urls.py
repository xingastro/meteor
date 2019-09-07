from django.urls import path

from . import views


app_name = 'meteor'
urlpatterns = [
    path('', views.index, name='index'),
    path('more/<str:book_name>', views.more, name='more'),
    path('search/', views.search, name='search'),
    path('cars/', views.cars, name='cars'),
    path('add_book/', views.add_book, name='add_book'),
    path('del_book/', views.del_book, name='del_book'),
    path('buy/', views.buy, name='buy'),
]
