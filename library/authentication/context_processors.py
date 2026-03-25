from django.apps import apps
from django.contrib.auth import get_user_model


def footer_counts(request):
    """Provide counts for footer: total books, orders, visitors, authors."""
    Book = apps.get_model('book', 'Book')
    Order = apps.get_model('order', 'Order')
    Author = apps.get_model('author', 'Author')
    CustomUser = get_user_model()

    try:
        books_count = Book.objects.count()
    except Exception:
        books_count = 0
    try:
        orders_count = Order.objects.count()
    except Exception:
        orders_count = 0
    try:
        visitors_count = CustomUser.objects.filter(role=0).count()
    except Exception:
        visitors_count = 0
    try:
        authors_count = Author.objects.count()
    except Exception:
        authors_count = 0

    return {
        "books_count": books_count,
        "orders_count": orders_count,
        "visitors_count": visitors_count,
        "authors_count": authors_count,
    }
