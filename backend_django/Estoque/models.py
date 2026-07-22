from django.db import models

from Medicamento.models import Medicamento
from EstabelecimentoSaude.models import EstabelecimentoSaude


class Estoque(models.Model):
    quantidade = models.IntegerField(default=0)

    medicamento = models.ForeignKey(
        Medicamento,
        on_delete=models.CASCADE,
        db_column="medicamento_catmat",
        related_name="estoques",
    )

    estabelecimento = models.ForeignKey(
        EstabelecimentoSaude,
        on_delete=models.CASCADE,
        related_name="estoques",
    )

    class Meta:
        db_table = "estoque"

        constraints = [
            models.UniqueConstraint(
                fields=["medicamento", "estabelecimento"],
                name="_medicamento_estabelecimento_uc",
            )
        ]

    def __str__(self):
        return f"{self.medicamento} - {self.estabelecimento}"