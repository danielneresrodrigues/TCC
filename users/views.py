from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from users.models import CustomUser
from django.urls import reverse_lazy
from .forms import CustomUserCreateForm

class CustomUserList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    
    group_required = 'admin'
    model = CustomUser
    template_name = 'users/listas/CustomUser.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        context['titulo'] = 'Usuários'
        context['titulo_conteudo_superior'] = 'Usuários'
        context['paragrafo_conteudo_superior'] = 'Lista de usuários cadastrados'

        return context
    
class CustomUserCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):

    group_required = 'admin'
    form_class = CustomUserCreateForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('listar-usuarios')

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        context['titulo'] = 'Cadastrar usuário'
        context['botao'] = 'Cadastrar'
        context['h3'] = 'Cadastrar usuário'
        context['h7'] = 'Certifique-se de que todos os campos obrigatórios estejam preenchidos corretamente.'

        return context

class CustomUserUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):

    group_required = 'admin'
    model = CustomUser
    
    fields = [
        'first_name','last_name','cpf','email',
        'entrada','saida','almoco','tipo','status','administrador'
        ]
    
    template_name = 'users/form.html'
    success_url = reverse_lazy('listar-usuarios')

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        context['titulo'] = 'Editar usuário'
        context['botao'] = 'Salvar'
        context['h3'] = 'Atualizar usuário'
        context['h7'] = 'Certifique-se de que todos os campos obrigatórios estejam preenchidos corretamente.'

        return context
    
    def get(self, request, *args, **kwargs):

        print(kwargs)

        return super().get(request, *args, **kwargs)
    
class CustomUserDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    
    group_required = 'admin'
    model = CustomUser
    template_name = 'users/form.html'
    success_url = reverse_lazy('listar-usuarios')

    def get_context_data(self, **kwargs):
        
        nome = kwargs['object']

        context = super().get_context_data(**kwargs)
        
        context['titulo'] = 'Excluir usuário'
        context['botao'] = 'Excluir'
        context['h3'] = 'Excluir usuário'
        context['h7'] = f'Deseja realmente excluir o usuario {nome}?'

        return context