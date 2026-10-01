from django.db import models


class EstabelecimentoSaude(models.Model):
    """
    Model que representa uma Unidade de Saúde da Família (USF / UBS)
    com base nas informações da SESAU Campo Grande.
    """
    cnes = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        verbose_name="CNES",
    )
    nome = models.CharField(
        max_length=255, 
        verbose_name="Nome da Unidade",
        help_text="Nome da Unidade de Saúde"
    )
    gestor = models.CharField(
        max_length=150, 
        blank=True, 
        null=True, 
        verbose_name="Gestor(a)",
        help_text="Nome do gestor responsável"
    )
    telefone = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Telefone(s)",
        help_text="Telefone(s) de contato ou gerência"
    )
    email = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="E-mail(s)",
        help_text="E-mail(s) de contato da unidade"
    )
    endereco = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Endereço",
        help_text="Endereço completo, bairro e CEP"
    )
    latitude = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Latitude",
        help_text="Coordenada geográfica da unidade em latitude"
    )
    longitude = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Longitude",
        help_text="Coordenada geográfica da unidade em longitude"
    )
    horario = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Horário de Funcionamento",
        help_text="Horário geral de funcionamento da unidade"
    )
    farmaceutico = models.BooleanField(
        default=False,
        verbose_name="Possui farmacêutico",
    )
    horario_farmaceutico = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Horário do farmacêutico",
    )
    competencias = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Competências / Informações Adicionais",
        help_text="Contém horários específicos como coleta laboratorial e salas de vacina (aceita marcação HTML)"
    )
    link = models.URLField(
        max_length=500, 
        blank=True, 
        null=True, 
        verbose_name="Link Oficial",
        help_text="Link para a página oficial da unidade"
    )

    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Unidade de Saúde"
        verbose_name_plural = "Unidades de Saúde"
        ordering = ['nome']

    def __str__(self):
        return self.nome