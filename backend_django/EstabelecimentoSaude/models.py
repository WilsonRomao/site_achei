from django.contrib.gis.db import models


class EstabelecimentoSaude(models.Model):
    cnes = models.CharField(max_length=7, primary_key=True)
    nome = models.TextField(unique=True)
    local = models.PointField()
    horario_abertura = models.TimeField()
    horario_fechamento = models.TimeField()
    descricao = models.TextField()  

    class Meta:
        db_table = "estabelecimento_saude"
        verbose_name = "Estabelecimento de Saúde"
        verbose_name_plural = "Estabelecimentos de Saúde"

    def __str__(self):
        return self.nome