from django.urls import path
from . import views

app_name = "author"

urlpatterns = [
    path("authors/", views.authors_list_view, name="authors_list"),
    path("authors/<int:author_id>/", views.author_detail_view, name="author_detail"),
    path("add/", views.add_author_view, name="add_author"),
    path("edit/<int:author_id>/", views.edit_author_view, name="edit_author"),
    path('delete/<int:author_id>/', views.delete_author_view, name='delete_author'),
]
