from django.contrib import admin
from .models import Order
from .models import Book
from .models import CustomUser


def order_str(self):
    return f"Order №{self.pk}"


Order.__str__ = order_str


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'book_display',
        'user_display',
        'created_at',
        'plated_end_at',
        'end_at',
        'is_returned',
        'is_overdue',
    )

    list_filter = (
        'book',
        'user',
        'created_at',
        'end_at',
        'plated_end_at',
    )

    search_fields = (
        'book__name',
        'user__email',
        'user__first_name',
        'user__last_name',
    )

    readonly_fields = ('created_at',)

    fieldsets = (
        ('Order information (static)', {
            'fields': ('book', 'user', 'created_at', 'plated_end_at'),
        }),
        ('Order status (changing)', {
            'fields': ('end_at',),
        }),
    )

    def book_display(self, obj):
        book = obj.book
        authors = ", ".join(a.surname for a in book.authors.all())
        return f"{book.name} ({authors})" if authors else book.name

    book_display.short_description = 'Book'

    def user_display(self, obj):
        user = obj.user
        if not user:
            return f"User №{obj.user_id}"
        full_name = " ".join(
            part for part in [user.first_name, user.middle_name, user.last_name] if part
        ).strip()
        if full_name:
            return full_name
        return user.email or f"User №{user.id}"

    user_display.short_description = 'User'

    def is_returned(self, obj):
        return obj.end_at is not None

    is_returned.boolean = True
    is_returned.short_description = 'Returned'

    def is_overdue(self, obj):
        if obj.end_at is not None or obj.plated_end_at is None:
            return False
        from django.utils import timezone
        return obj.plated_end_at < timezone.now()

    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Customize how book and user are displayed in the admin form dropdowns,
        WITHOUT changing __str__ of the models.
        """
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "book":
            def label_from_instance(book: Book):
                authors = ", ".join(a.surname for a in book.authors.all())
                return f"{book.name} ({authors})" if authors else book.name

            formfield.label_from_instance = label_from_instance

        elif db_field.name == "user":
            def label_from_instance(user: CustomUser):
                full_name = " ".join(
                    part
                    for part in [user.first_name, user.middle_name, user.last_name]
                    if part
                ).strip()
                if full_name and user.email:
                    return full_name
                if user.email:
                    return user.email
                if full_name:
                    return full_name
                return f"User №{user.id}"

            formfield.label_from_instance = label_from_instance

        return formfield
