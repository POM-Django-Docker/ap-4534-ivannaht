"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from authentication.views import home_view, UserViewSet, UserRegistrationAPIView
from rest_framework.routers import DefaultRouter
from book.views import BookViewSet
from order.views import OrderViewSet
from author.views import AuthorViewSet

api_router = DefaultRouter()
api_router.register(r'book', BookViewSet, basename='api_book')
api_router.register(r'order', OrderViewSet, basename='api_order')
api_router.register(r'user/(?P<user_id>\d+)/order', OrderViewSet, basename='api_user_order')
api_router.register(r"user", UserViewSet, basename="api_user"),
api_router.register(r"author", AuthorViewSet, basename="api_author")


urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path("auth/", include("authentication.urls", namespace="authentication")),
    path('author/', include('author.urls', namespace='author')),
    path("book/", include("book.urls", namespace="book")),
    path("order/", include("order.urls", namespace="order")),
    path("api/v1/user/register/", UserRegistrationAPIView.as_view(), name="api_user_create"),
    path("api/v1/", include(api_router.urls)),
]
