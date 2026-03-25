from django import forms

from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.ModelForm):
    """
    Register a new CustomUser (visitor or librarian).
    Uses ModelForm + extra password fields.
    """
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter password",
            "class": "form-input",
        }),
    )
    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Repeat password",
            "class": "form-input",
        }),
    )

    class Meta:
        model = User
        fields = ["first_name", "middle_name", "last_name", "email", "role"]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "maxlength": 20,
                "class": "form-input",
                "placeholder": "Enter first name",
            }),
            "middle_name": forms.TextInput(attrs={
                "maxlength": 20,
                "class": "form-input",
                "placeholder": "Enter middle name",
            }),
            "last_name": forms.TextInput(attrs={
                "maxlength": 20,
                "class": "form-input",
                "placeholder": "Enter last name",
            }),
            "email": forms.EmailInput(attrs={
                "maxlength": 100,
                "class": "form-input",
                "placeholder": "Enter Email",
            }),
            "role": forms.Select(attrs={
                "class": "form-select",
            }),
        }

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            raise forms.ValidationError("Email is required.")

        if len(email) > 100:
            raise forms.ValidationError("Email must be at most 100 characters.")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")

        return email

    def clean_first_name(self):
        first_name = (self.cleaned_data.get("first_name") or "").strip()
        if first_name and len(first_name) > 20:
            raise forms.ValidationError("First name must be at most 20 characters.")
        return first_name

    def clean_middle_name(self):
        middle_name = (self.cleaned_data.get("middle_name") or "").strip()
        if middle_name and len(middle_name) > 20:
            raise forms.ValidationError("Middle name must be at most 20 characters.")
        return middle_name

    def clean_last_name(self):
        last_name = (self.cleaned_data.get("last_name") or "").strip()
        if last_name and len(last_name) > 20:
            raise forms.ValidationError("Last name must be at most 20 characters.")
        return last_name

    def clean_role(self):
        role = self.cleaned_data.get("role")
        if role not in (0, 1):
            raise forms.ValidationError("Invalid role selected.")
        return role

    def clean(self):
        """
        Cross-field validation for passwords.
        If this raises ValidationError, form.is_valid() == False.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if not password1 or not password2:
            raise forms.ValidationError("Both password fields are required.")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        """
        Override save to use create_user / set_password properly.
        """
        user = super().save(commit=False)
        password = self.cleaned_data["password1"]

        user.set_password(password)
        user.is_active = True

        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """
    Form for logging in an existing users
    """
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter your email"
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password"
        })
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        return email


class EditProfileForm(forms.ModelForm):
    """
    Form for editing the logged-in user's profile.
    No password or role change here (for safety).
    """

    class Meta:
        model = User
        fields = ["first_name", "middle_name", "last_name"]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "maxlength": 20,
                "class": "form-input",
                "placeholder": "Enter first name",
            }),
            "middle_name": forms.TextInput(attrs={
                "maxlength": 20,
                "class": "form-input",
                "placeholder": "Enter middle name",
            }),
            "last_name": forms.TextInput(attrs={
                "maxlength": 20,
                "class": "form-input",
                "placeholder": "Enter last name",
            }),
        }

    def clean_first_name(self):
        first_name = (self.cleaned_data.get("first_name") or "").strip()
        if first_name and len(first_name) > 20:
            raise forms.ValidationError("First name must be at most 20 characters.")
        return first_name

    def clean_middle_name(self):
        middle_name = (self.cleaned_data.get("middle_name") or "").strip()
        if middle_name and len(middle_name) > 20:
            raise forms.ValidationError("Middle name must be at most 20 characters.")
        return middle_name

    def clean_last_name(self):
        last_name = (self.cleaned_data.get("last_name") or "").strip()
        if last_name and len(last_name) > 20:
            raise forms.ValidationError("Last name must be at most 20 characters.")
        return last_name
