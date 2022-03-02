from django.urls import path 
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'),
    path('category/<str:id>/', views.category, name='category'),
    path('rooms/',views.rooms, name='rooms'),
    path('details/<str:id>/',views.details, name='details'),
    path('booking_view/',views.booking_view, name='booking_view'),
    path('booking/',views.booking, name='booking'),
    path('login/', views.loginform, name='loginform'),
    path('logoutform/', views.logoutfunc, name='logoutfunc'),
    path('signup/', views.signupform, name='signupform'),
    path('password/',views.password, name='password'),
    path('checkout/',views.checkout, name='checkout'),
    path('placeorder/',views.placeorder, name='placeorder'),
    path('completed/',views.completed, name='completed'),
    path('deleteitem/',views.deleteitem, name='deleteitem'),
    path('increase/', views.increase, name='increase'),
    
]