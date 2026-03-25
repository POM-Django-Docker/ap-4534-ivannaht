from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import OrderCreateForm, OrderEditForm
from book.models import Book
from .models import Order
from rest_framework import viewsets
from .serializers import OrderSerializer



@login_required
def order_list(request):
    if request.user.role == 1:
        orders = Order.objects.select_related("book", "user").all().order_by("-created_at")
    else:
        orders = Order.objects.select_related("book", "user").filter(user=request.user).order_by("-created_at")

    return render(request, "order/order_list.html", {"orders": orders})


@login_required
def my_orders(request):
    orders = Order.objects.select_related("book").filter(user=request.user).order_by("-created_at")
    return render(request, "order/my_orders.html", {"orders": orders})


@login_required
def create_order(request):
    if request.method == "POST":
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.plated_end_at = timezone.now() + timedelta(days=14)

            book = order.book
            if book.count < 1:
                return render(request, "order/order_form.html", {
                    "form": form,
                    "is_edit": False,
                    "error": "This book is not available now."
                })

            order.save()
            book.count -= 1
            book.save()

            return redirect("order:my_orders")
    else:
        form = OrderCreateForm()

    return render(request, "order/order_form.html", {
        "form": form,
        "is_edit": False
    })


@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.user != request.user and request.user.role != 1:
        return render(request, "book/access_denied.html", status=403)

    if order.end_at:
        return render(request, "book/access_denied.html", status=403)

    if request.method == "POST":
        form = OrderEditForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            return redirect("order:my_orders")
    else:
        form = OrderEditForm(instance=order)

    return render(request, "order/order_form.html", {
        "form": form,
        "order": order,
        "is_edit": True
    })


@login_required
def close_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    is_librarian = request.user.role == 1
    is_owner = order.user == request.user

    if not is_librarian and not is_owner:
        return HttpResponseForbidden("You cannot close this order.")

    if order.end_at is not None:
        if is_librarian:
            return redirect("order:order_list")
        return redirect("order:my_orders")

    order.end_at = timezone.now()
    order.save()

    book = order.book
    book.count += 1
    book.save()

    if is_librarian:
        return redirect("order:order_list")
    return redirect("order:my_orders")

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id is not None:
            return Order.objects.filter(user_id=user_id)
        return Order.objects.all()
