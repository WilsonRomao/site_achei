from rest_framework import serializers

from .models import Estoque


class EstoqueSerializer(serializers.ModelSerializer):
    catmat = serializers.SerializerMethodField()
    medicamento = serializers.SerializerMethodField()
    estabelecimentoSaude = serializers.SerializerMethodField()

    class Meta:
        model = Estoque
        fields = ["catmat", "medicamento", "quantidade", "estabelecimentoSaude"]

    def get_catmat(self, obj):
        return obj.medicamento.catmat

    def get_medicamento(self, obj):
        return obj.medicamento.medicamento

    def get_estabelecimentoSaude(self, obj):
        return obj.estabelecimento.nome
