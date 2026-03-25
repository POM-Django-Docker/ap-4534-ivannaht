from django.urls import path
from . import views

app_name = "authentication"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("users/", views.users_list_view, name="users_list"),
    path("users/<int:user_id>/", views.user_detail_view, name="user_detail"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit_view, name="profile_edit")
]
