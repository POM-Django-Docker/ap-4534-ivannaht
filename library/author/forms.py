from django import forms
from .models import Author


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "patronymic", "surname", "books"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "register-input"
            }),
            "patronymic": forms.TextInput(attrs={
                "class": "register-input"
            }),
            "surname": forms.TextInput(attrs={
                "class": "register-input"
            }),
            "books": forms.SelectMultiple(attrs={
                "class": "register-input"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].required = True
        self.fields['surname'].required = True

        self.fields["name"].error_messages["required"] = "Name cannot be empty."
        self.fields["surname"].error_messages["required"] = "Surname cannot be empty."
