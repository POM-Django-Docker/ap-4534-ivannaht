from django import forms

from .models import Book
from author.models import Author


class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        required=False
    )

    class Meta:
        model = Book
        fields = ["name", "description", "count"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields["authors"].initial = self.instance.authors.all()

    def save(self, commit=True):
        authors = self.cleaned_data.pop("authors")
        book = super().save(commit=commit)

        if commit:
            book.authors.set(authors)
        else:
            self._authors = authors

        return book

    def save_m2m(self):
        super().save_m2m()
        if hasattr(self, "_authors"):
            self.instance.authors.set(self._authors)