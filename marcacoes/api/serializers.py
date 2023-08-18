from rest_framework.serializers import ModelSerializer
from marcacoes.models import Marcacoes

class MarcacoesSerializer(ModelSerializer):

    class Meta:
        model = Marcacoes
        fields = '__all__'