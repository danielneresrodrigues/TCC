from django.urls import path
from .views import CustomUserList, CustomUserCreate, CustomUserUpdate, CustomUserDelete
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page = 'inicio'), name = 'logout'),
    path('listar/', CustomUserList.as_view(), name = 'listar-usuarios'),
    path('criar/', CustomUserCreate.as_view(), name = 'criar-usuario'),
    path('editar/<int:pk>', CustomUserUpdate.as_view(), name = 'editar-usuario'),
    path('excluir/<int:pk>', CustomUserDelete.as_view(), name = 'excluir-usuario'),
]