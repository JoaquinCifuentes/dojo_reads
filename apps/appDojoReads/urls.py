from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('registro/', views.registro, name="registro"),
    path('login/', views.login, name="login"),
    path('books/', views.books, name="books"),
    path('add/', views.add, name="add"),
    path('addReview/<int:libroId>', views.addReview, name="addReview"),
    path('detalle/<int:libroId>', views.detalle, name="detalle"),
    path('usuario/<int:id>', views.usuario, name="usuario"),
    path('delete/', views.delete, name="delete"),
    path('salir/', views.salir, name="salir"),
]