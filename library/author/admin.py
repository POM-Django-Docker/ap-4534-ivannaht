from django.contrib import admin
from django import forms
from .models import Author
from .models import Book


def author_str(self):
    full_name = f"{self.name} {self.patronymic} {self.surname}"
    return full_name


Author.__str__ = author_str


class AuthorAdminForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def book_label(book: Book):
            authors = ", ".join(a.surname for a in book.authors.all())
            return f"{book.name} ({authors})" if authors else book.name

        self.fields['books'].label_from_instance = book_label


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    form = AuthorAdminForm

    list_display = ('id', 'name', 'surname', 'patronymic')
    list_filter = ('surname',)
    search_fields = ('name', 'surname', 'patronymic')
    filter_horizontal = ('books',)

    fieldsets = (
        ('Personal information', {
            'fields': ('name', 'surname', 'patronymic'),
        }),
        ('Books', {
            'fields': ('books',),
        }),
    )

    filter_horizontal = ('books',)

    def books_count(self, obj):
        """Number of books this author is linked to."""
        return obj.books.count()

    books_count.short_description = 'Books count'
