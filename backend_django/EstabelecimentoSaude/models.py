from django.db import models


class EstabelecimentoSaude(models.Model):
    nome = models.TextField(unique=True)

    class Meta:
        db_table = "estabelecimento_saude"
        verbose_name = "Estabelecimento de Saúde"
        verbose_name_plural = "Estabelecimentos de Saúde"

    def __str__(self):
        return self.nome