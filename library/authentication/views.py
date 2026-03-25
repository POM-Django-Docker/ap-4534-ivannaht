from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from order.models import Order
from book.models import Book
from .forms import RegisterForm
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from rest_framework import viewsets, permissions
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

User = get_user_model()


def home_view(request):
    return render(request, "home.html")


def register_view(request):
    """
    Register a new CustomUser as visitor (0) or librarian (1)
    using a plain HTML form.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = RegisterForm()

    context = {
        "form": form,
    }
    return render(request, "authentication/register.html", context)


def login_view(request):
    """
    Log in a user by email and password (visitor or librarian).
    """
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)

            if user is not None:
                if not user.is_active:
                    form.add_error(None, "Your account is not active.")
                else:
                    login(request, user)
                    return redirect("home")
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = LoginForm()

    context = {
        "form": form,
    }
    return render(request, "authentication/login.html", context)


def logout_view(request):
    """
    Log out currently authenticated user.
    """
    logout(request)

    return redirect("home")


def users_list_view(request):
    """
    Show a list of all users. Only accessible to librarians (role == 1).
    """
    if not request.user.is_authenticated:
        from django.contrib import messages

        messages.error(request, "You must be logged in to view users.")
        return redirect("authentication:login")

    if getattr(request.user, "role", 0) != 1:
        from django.http import HttpResponseForbidden

        return HttpResponseForbidden("You do not have permission to view this page.")

    users = User.objects.all().order_by("id")
    context = {"users": users}
    return render(request, "authentication/users_list.html", context)


def user_detail_view(request, user_id):
    """
    Show details for a single user. Only accessible to librarians (role == 1).
    """
    if not request.user.is_authenticated:
        from django.contrib import messages

        messages.error(request, "You must be logged in to view user details.")
        return redirect("authentication:login")

    if getattr(request.user, "role", 0) != 1:
        from django.http import HttpResponseForbidden

        return HttpResponseForbidden("You do not have permission to view this page.")

    try:
        u = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        from django.http import Http404

        raise Http404("User not found")

    context = {"user_obj": u}
    if getattr(u, "role", 0) == 0:
        orders = Order.objects.filter(user=u).order_by("-created_at")
        books = Book.objects.filter(order__user=u).distinct()
        context.update({"orders": orders, "books": books})
    return render(request, "authentication/user_detail.html", context)


@login_required
def profile_view(request):
    """
    Display the logged-in user's profile.
    """
    user_obj = request.user
    orders = None
    books = None

    if user_obj.role == 0:
        orders = Order.objects.filter(user=user_obj).order_by("-created_at")
        books = Book.objects.filter(order__user=user_obj).distinct()

    context = {
        "user_obj": user_obj,
        "orders": orders,
        "books": books,
    }
    return render(request, "authentication/profile.html", context)


@login_required
def profile_edit_view(request):
    """
    Edit the logged-in user's profile.
    """
    user = request.user

    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("authentication:profile")
    else:
        form = EditProfileForm(instance=user)

    return render(request, "authentication/profile_edit.html", {"form": form, "user_obj": user})


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing CustomUser instances via REST API.
    """
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
