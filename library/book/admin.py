from django.contrib import admin
from .models import Book


def book_str(self):
    return f"{self.name} (id={self.id})"


Book.__str__ = book_str


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'count',
        'authors_list',
    )

    list_filter = (
        'count',
    )

    search_fields = (
        'name',
        'description',
        'authors__name',
        'authors__surname',
    )

    fieldsets = (
        ('Static information (not changing)', {
            'fields': ('name', 'description'),
        }),
        ('Dynamic / inventory information', {
            'fields': ('count',),
        }),
    )

    def authors_list(self, obj):
        """Show authors linked to this book."""
        authors = obj.authors.all()
        if not authors:
            return "—"
        return ", ".join(f"{a.name} {a.surname}" for a in authors)

    authors_list.short_description = "Authors"
