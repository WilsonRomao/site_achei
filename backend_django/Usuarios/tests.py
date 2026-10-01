from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import SolicitacaoPerfil, Usuario
from .importers import importar_usuarios


class UsuarioAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user_creates_account(self):
        payload = {
            "email": "novo@teste.com",
            "password": "senha1234",
        }

        response = self.client.post(
            reverse("register"),
            payload,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Usuario.objects.filter(email="novo@teste.com").exists())

    def test_login_returns_token_for_valid_credentials(self):
        Usuario.objects.create_user(email="login@teste.com", password="senha1234")

        response = self.client.post(
            reverse("login"),
            {"email": "login@teste.com", "senha": "senha1234"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())
        self.assertEqual(response.json()["usuario"]["email"], "login@teste.com")

    def test_login_rejects_invalid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {"email": "naoexiste@teste.com", "senha": "errada"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)

    def test_login_rejects_inactive_user(self):
        user = Usuario.objects.create_user(email="inativo@teste.com", password="senha1234")
        user.is_active = False
        user.save(update_fields=["is_active"])

        response = self.client.post(
            reverse("login"),
            {"email": "inativo@teste.com", "senha": "senha1234"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)

    def test_csv_import_cannot_create_superuser(self):
        importar_usuarios(SimpleUploadedFile(
            "usuarios.csv",
            b"email,senha,perfis,is_staff,is_superuser,is_active\n"
            b"csv@teste.com,senha1234,administrador,true,true,true\n",
        ))

        usuario = Usuario.objects.get(email="csv@teste.com")
        self.assertTrue(usuario.is_staff)
        self.assertFalse(usuario.is_superuser)

    def test_admin_user_list_requires_admin_profile(self):
        user = Usuario.objects.create_user(email="padrao@teste.com", password="senha1234")
        user.perfis = ["padrão"]
        user.save(update_fields=["perfis"])

        self.client.force_authenticate(user=user)
        response = self.client.get(reverse("admin-usuarios"))

        self.assertEqual(response.status_code, 403)

    def test_solicitacao_de_perfil_creates_pending_request(self):
        user = Usuario.objects.create_user(email="solicitante@teste.com", password="senha1234")
        self.client.force_authenticate(user=user)

        response = self.client.post(
            reverse("solicitar-perfil"),
            {"perfil": "administrador"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            SolicitacaoPerfil.objects.filter(
                usuario=user,
                perfil_solicitado="administrador",
                status="pendente",
            ).exists()
        )

    def test_admin_can_list_users(self):
        admin = Usuario.objects.create_user(email="admin@teste.com", password="senha1234")
        admin.perfis = ["administrador"]
        admin.save(update_fields=["perfis"])

        self.client.force_authenticate(user=admin)
        response = self.client.get(reverse("admin-usuarios"))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_admin_can_approve_user_profile_request(self):
        admin = Usuario.objects.create_user(email="admin2@teste.com", password="senha1234")
        admin.perfis = ["administrador"]
        admin.save(update_fields=["perfis"])

        user = Usuario.objects.create_user(email="usuario2@teste.com", password="senha1234")
        solicitacao = SolicitacaoPerfil.objects.create(
            usuario=user,
            perfil_solicitado="administrador",
            status="pendente",
        )

        self.client.force_authenticate(user=admin)
        response = self.client.post(
            reverse("admin-solicitacao-action", args=[solicitacao.pk, "aprovar"]),
        )

        self.assertEqual(response.status_code, 200)
        solicitacao.refresh_from_db()
        self.assertEqual(solicitacao.status, "aprovado")
        user.refresh_from_db()
        self.assertIn("administrador", user.perfis)
