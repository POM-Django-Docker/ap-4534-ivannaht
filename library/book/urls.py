from django.urls import path
from . import views

app_name = "book"

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path("user/<int:user_id>/", views.books_by_user, name="books_by_user"),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path("add/", views.create_book, name="create_book"),
    path("<int:book_id>/edit/", views.edit_book, name="edit_book"),
]