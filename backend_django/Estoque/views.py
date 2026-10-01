from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from EstabelecimentoSaude.models import EstabelecimentoSaude
from Medicamento.models import Medicamento
from .models import Estoque
from .serializers import EstoqueSerializer


class EstoqueListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Estoque.objects.select_related("medicamento", "estabelecimento")

        catmat = request.query_params.get("catmat")
        estabelecimento = request.query_params.get("estabelecimento")
        q = request.query_params.get("q")

        if catmat:
            queryset = queryset.filter(medicamento__catmat__icontains=catmat)
        if estabelecimento:
            queryset = queryset.filter(estabelecimento__nome__icontains=estabelecimento)
        if q:
            queryset = queryset.filter(medicamento__medicamento__icontains=q)

        try:
            page = max(int(request.query_params.get("page", 1)), 1)
            per_page = min(max(int(request.query_params.get("per_page", 20)), 1), 100)
        except ValueError:
            return Response({"message": "Parâmetros de paginação inválidos."}, status=status.HTTP_400_BAD_REQUEST)

        total = queryset.count()
        start = (page - 1) * per_page
        end = start + per_page
        page_items = queryset[start:end]

        serializer = EstoqueSerializer(page_items, many=True, context={"request": request})

        return Response(
            {
                "items": serializer.data,
                "total": total,
                "pages": (total + per_page - 1) // per_page if per_page else 1,
                "current_page": page,
                "has_next": end < total,
                "has_prev": page > 1,
            },
            status=status.HTTP_200_OK,
        )
