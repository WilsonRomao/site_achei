from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from EstabelecimentoSaude.models import EstabelecimentoSaude
from Medicamento.models import Medicamento
from Usuarios.models import Usuario
from .models import Estoque


class EstoquePublicApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_estoque_endpoint_returns_items(self):
        estabelecimento = EstabelecimentoSaude.objects.create(nome="UBS Teste")
        medicamento = Medicamento.objects.create(catmat="BR123", medicamento="Aspirina")
        Estoque.objects.create(medicamento=medicamento, estabelecimento=estabelecimento, quantidade=12)

        response = self.client.get(reverse("estoque-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total"], 1)
        self.assertEqual(response.json()["items"][0]["medicamento"], "Aspirina")
        self.assertEqual(response.json()["items"][0]["disponibilidade"], "Disponível")
        self.assertNotIn("quantidade", response.json()["items"][0])

    def test_authenticated_user_can_see_exact_quantity(self):
        estabelecimento = EstabelecimentoSaude.objects.create(nome="UBS Autenticada")
        medicamento = Medicamento.objects.create(catmat="BR124", medicamento="Aspirina")
        Estoque.objects.create(medicamento=medicamento, estabelecimento=estabelecimento, quantidade=12)
        user = Usuario.objects.create_user(email="estoque@teste.com", password="senha1234")

        self.client.force_authenticate(user=user)
        response = self.client.get(reverse("estoque-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["items"][0]["quantidade"], 12)

    def test_estoque_can_be_filtered_by_catmat(self):
        estabelecimento = EstabelecimentoSaude.objects.create(nome="UBS Filtro")
        medicamento = Medicamento.objects.create(catmat="BR999", medicamento="Dipirona")
        Estoque.objects.create(medicamento=medicamento, estabelecimento=estabelecimento, quantidade=7)

        response = self.client.get(reverse("estoque-list") + "?catmat=BR999")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total"], 1)
        self.assertEqual(response.json()["items"][0]["catmat"], "BR999")
