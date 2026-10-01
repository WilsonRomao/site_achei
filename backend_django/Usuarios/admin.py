from django.contrib import admin
from django import forms
from django.urls import path

from config.admin_csv import csv_download_response, render_csv_upload

from .importers import importar_usuarios
from .models import SolicitacaoPerfil, Usuario


class UsuarioCreationForm(forms.ModelForm):
	password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Confirme a senha", widget=forms.PasswordInput)

	class Meta:
		model = Usuario
		fields = ("email", "perfis", "is_staff", "is_superuser")

	def clean(self):
		cleaned_data = super().clean()
		if cleaned_data.get("password1") != cleaned_data.get("password2"):
			raise forms.ValidationError("As senhas não coincidem.")
		return cleaned_data

	def save(self, commit=True):
		usuario = super().save(commit=False)
		usuario.set_password(self.cleaned_data["password1"])
		if commit:
			usuario.save()
		return usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
	add_form = UsuarioCreationForm
	change_list_template = "admin/Usuarios/change_list.html"
	list_display = ("email", "is_staff", "is_superuser", "is_active")
	list_filter = ("is_staff", "is_superuser", "is_active")
	search_fields = ("email",)
	ordering = ("email",)
	fieldsets = (
		(None, {"fields": ("email", "password")}),
		("Permissoes", {"fields": ("perfis", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
		("Datas importantes", {"fields": ("last_login", "date_joined")} ),
	)
	add_fieldsets = (
		(None, {
			"classes": ("wide",),
			"fields": ("email", "password1", "password2", "perfis", "is_staff", "is_superuser"),
		}),
	)

	def get_urls(self):
		urls = super().get_urls()
		custom_urls = [
			path("importar-csv/", self.admin_site.admin_view(self.importar_csv), name="usuario_importar_csv"),
			path("modelo-csv/", self.admin_site.admin_view(self.modelo_csv), name="usuario_modelo_csv"),
		]
		return custom_urls + urls

	def importar_csv(self, request):
		return render_csv_upload(
			self,
			request,
			"Importar usuários",
			"modelo-csv/",
			importar_usuarios,
		)

	def modelo_csv(self, request):
		return csv_download_response(
			"modelo_usuarios.csv",
			["email", "senha", "perfis", "is_staff", "is_superuser", "is_active"],
			["usuario@exemplo.com", "senha1234", "padrão|prescritor", "false", "false", "true"],
		)


@admin.register(SolicitacaoPerfil)
class SolicitacaoPerfilAdmin(admin.ModelAdmin):
	list_display = ("usuario", "perfil_solicitado", "status", "data_solicitacao")
	list_filter = ("status", "perfil_solicitado")
	search_fields = ("usuario__email",)
	ordering = ("-data_solicitacao",)
