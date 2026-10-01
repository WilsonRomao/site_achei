from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import EstabelecimentoSaude


class EstabelecimentoListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        estabelecimentos = EstabelecimentoSaude.objects.order_by("nome").all()
        unidades = [
            {
                "id": item.id,
                "cnes": item.cnes,
                "nome": item.nome,
                "gestor": item.gestor,
                "telefone": item.telefone,
                "email": item.email,
                "endereco": item.endereco,
                "latitude": item.latitude,
                "longitude": item.longitude,
                "horario": item.horario,
                "farmaceutico": item.farmaceutico,
                "horario_farmaceutico": item.horario_farmaceutico,
                "competencias": item.competencias,
                "link": item.link,
            }
            for item in estabelecimentos
        ]
        return Response(unidades, status=status.HTTP_200_OK)
