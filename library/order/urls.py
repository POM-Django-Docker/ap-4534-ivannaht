from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("", views.order_list, name="order_list"),
    path("my/", views.my_orders, name="my_orders"),
    path("create/", views.create_order, name="create_order"),
    path("close/<int:order_id>/", views.close_order, name="close_order"),
    path("create/", views.create_order, name="create_order"),
    path("<int:order_id>/edit/", views.edit_order, name="edit_order"),
]