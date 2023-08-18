from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, Tipo, Status

class CustomUserAdmin(UserAdmin):
    save_on_top = True

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'cpf')}),
        ('Jornada', {'fields': ('entrada', 'saida', 'almoco')}),
        ('Situação atual', {'fields': ('tipo', 'status')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'last_login')
    filter_horizontal = ['groups']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Tipo)
admin.site.register(Status)