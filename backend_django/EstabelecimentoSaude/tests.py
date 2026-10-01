import io

import pandas as pd
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import EstabelecimentoSaude
from .services import importar_unidades


class EstabelecimentoPublicApiTests(TestCase):
    def test_estabelecimentos_endpoint_returns_unit_data(self):
        EstabelecimentoSaude.objects.create(
            nome="UBS Centro",
            endereco="Rua A, 10",
            latitude=-20.4697,
            longitude=-54.6201,
            horario="07h às 19h",
        )
        EstabelecimentoSaude.objects.create(nome="Hospital Municipal")

        response = self.client.get(reverse("estabelecimentos-list"))

        self.assertEqual(response.status_code, 200)
        unidades = response.json()
        self.assertEqual(unidades[0]["nome"], "Hospital Municipal")
        self.assertEqual(unidades[1]["nome"], "UBS Centro")
        self.assertEqual(unidades[1]["latitude"], -20.4697)
        self.assertEqual(unidades[1]["endereco"], "Rua A, 10")

    def test_importa_planilha_infousf(self):
        arquivo = io.BytesIO()
        pd.DataFrame([
            {
                "CNES": 28851,
                "nome": "USF COOPHAVILA II - ALFREDO NEDER",
                "latitude": -20536059,
                "longitude": -54667429,
                "horarioFuncionamento": "segunda a sexta-feira 07 às 19h",
                "farmaceutico": "SIM",
                "horarioFarmaceutico": "segunda a sexta-feira 07 às 13h",
                "link": "https://example.org/unidade",
            }
        ]).to_excel(arquivo, index=False)
        arquivo.seek(0)

        resultado = importar_unidades(SimpleUploadedFile("InfoUSF.xlsx", arquivo.read()))
        unidade = EstabelecimentoSaude.objects.get(cnes="28851")

        self.assertEqual(resultado["criadas"], 1)
        self.assertEqual(unidade.nome, "USF COOPHAVILA II - ALFREDO NEDER")
        self.assertEqual(unidade.latitude, -20.536059)
        self.assertEqual(unidade.longitude, -54.667429)
        self.assertTrue(unidade.farmaceutico)
