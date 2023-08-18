from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreateForm(UserCreationForm):

    entrada = forms.TimeField(widget=forms.TimeInput)

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'cpf',
            'email',
            'entrada',
            'saida',
            'almoco',
            'tipo',
            'status',
            'administrador',
            'password1',
            'password2',
        ]