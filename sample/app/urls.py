from django.urls import path
from . import views

urlpatterns=[
    path('',views.shop_login),
    path('logout',views.shop_logout),
    path('shop_home',views.shop_home),
    path('add_car/', views.add_car),
    path('edit-car/<int:car_id>/', views.edit_car, name='edit_car'),
    path('delete_car/<int:id>/', views.delete_car, name='delete_car'),
    path('budget_cars/<id>',views.budget_cars),
    path('about',views.about),

    path('register',views.register),
    path('user_home',views.user_home),
    path('cars_list/<int:id>/', views.cars_list),

]