from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet
from datetime import date
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from marcacoes.api.serializers import MarcacoesSerializer
from marcacoes.models import Marcacoes

from rest_framework.permissions import IsAuthenticated

class CreateMarcacoesViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MarcacoesSerializer

    def create(self, request):
        user = request.user  # Obtém o usuário da requisição
        data_hora_atual = timezone.now()  # Obtém a data e hora atual

        # Obtém os valores de latitude e longitude da requisição
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        # Define os dados para a criação da marcação
        marcação_data = {
            'user': user.id,
            'data': data_hora_atual,
            'latitude': latitude,
            'longitude': longitude
        }

        # Cria a marcação
        serializer = self.serializer_class(data=marcação_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MarcacoesAtuaisViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MarcacoesSerializer
    queryset = Marcacoes.objects.all()

    def get_queryset(self):
        user = self.request.user  # Pega o usuário da requisição
        today = date.today()  # Obtém a data de hoje
        
        # Filtra as marcações do usuário atual na data de hoje
        queryset = Marcacoes.objects.filter(user=user, data__date=today)
        return queryset