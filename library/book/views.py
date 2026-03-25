from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from authentication.models import CustomUser
from order.models import Order
from django.db.models import Q
from .models import Book
from .forms import BookForm
from rest_framework import viewsets
from .serializers import BookSerializer



def book_list(request):
    title = request.GET.get("title", "").strip()
    author = request.GET.get("author", "").strip()
    sort = request.GET.get("sort")

    books = Book.objects.all()

    if title:
        books = books.filter(name__icontains=title)

    if author:
        books = books.filter(
            Q(authors__name__icontains=author) |
            Q(authors__surname__icontains=author) |
            Q(authors__patronymic__icontains=author)
        )

    allowed_sorts = ["id", "name", "count"]
    if sort not in allowed_sorts:
        sort = "id"

    books = books.order_by(sort).distinct()

    context = {
        "books": books,
        "title": title,
        "author": author,
        "sort": sort,
    }

    return render(request, "book/book_list.html", context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book/book_detail.html', {'book': book})

@login_required
def create_book(request):
    if request.user.role != 1 and not request.user.is_superuser:
        return render(request, "book/access_denied.html", status=403)

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book:book_list")
    else:
        form = BookForm()

    return render(request, "book/book_form.html", {"form": form, "is_edit": False})


@login_required
def edit_book(request, book_id):
    if request.user.role != 1 and not request.user.is_superuser:
        return render(request, "book/access_denied.html", status=403)

    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book:book_detail", book_id=book.id)
    else:
        form = BookForm(instance=book)

    return render(request, "book/book_form.html", {
        "form": form,
        "book": book,
        "is_edit": True,
    })

@login_required
def books_by_user(request, user_id):
    if request.user.role != 1 and not request.user.is_superuser:
        return render(request, "book/access_denied.html", status=403)

    user = get_object_or_404(CustomUser, id=user_id)

    orders = Order.objects.filter(user=user).select_related("book").order_by("-created_at")

    books = []
    seen_book_ids = set()

    for order in orders:
        if order.book.id not in seen_book_ids:
            books.append(order.book)
            seen_book_ids.add(order.book.id)

    context = {
        "target_user": user,
        "books": books,
        "orders": orders,
    }

    return render(request, "book/books_by_user.html", context)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
