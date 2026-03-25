from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["book"]


class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["plated_end_at"]
        widgets = {
            "plated_end_at": forms.DateTimeInput(attrs={"type": "datetime-local"})
        }