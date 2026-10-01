from django.test import TestCase
from django.urls import reverse

from .models import Medicamento


class MedicamentoPublicApiTests(TestCase):
    # esta função verifica se o endpoint de medicamentos retorna os itens paginados corretamente;
    def test_medicamentos_endpoint_returns_paginated_items(self):
        Medicamento.objects.create(catmat="123456", medicamento="Paracetamol")
        Medicamento.objects.create(catmat="654321", medicamento="Ibuprofeno")

        response = self.client.get(reverse("medicamentos-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total"], 2)
        self.assertIn("items", response.json())
        nomes = [item["medicamento"] for item in response.json()["items"]]
        self.assertIn("Paracetamol", nomes)
        self.assertIn("Ibuprofeno", nomes)
    # esta função verifica se o endpoint de medicamentos pode filtrar os itens pelo nome do medicamento;
    def test_medicamentos_can_be_filtered_by_name(self):
        Medicamento.objects.create(catmat="111", medicamento="Dipirona")
        Medicamento.objects.create(catmat="222", medicamento="Amoxicilina")

        response = self.client.get(reverse("medicamentos-list") + "?q=Dipirona")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total"], 1)
        self.assertEqual(response.json()["items"][0]["medicamento"], "Dipirona")
