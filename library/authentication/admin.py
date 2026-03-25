from django.contrib import admin
from django import forms
from .models import CustomUser, ROLE_CHOICES


def user_str(self):
    full_name = f"{self.first_name} {self.middle_name} {self.last_name}"
    return full_name


CustomUser.__str__ = user_str


class CustomUserAdminForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = '__all__'



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserAdminForm
    list_display = (
        'id',
        'email',
        'first_name',
        'middle_name',
        'last_name',
        'role',
        'is_active',
        'created_at',
        'updated_at',
        'role_name',
    )

    list_filter = (
        'role',
        'is_active',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'email',
        'first_name',
        'middle_name',
        'last_name',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Personal information', {
            'fields': (
                'first_name',
                'middle_name',
                'last_name',
                'email',
                'password',
            ),
        }),
        ('Status & role', {
            'fields': (
                'role',
                'is_active',
            ),
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            ),
        }),
    )

    def role_name(self, obj):
        """Human‑readable name for the role."""
        return obj.get_role_name()

    role_name.short_description = 'Role name'
