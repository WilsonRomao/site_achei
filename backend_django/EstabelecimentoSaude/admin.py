from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import path
from django import forms

from .models import EstabelecimentoSaude
from .services import importar_unidades


class UploadUnidadesForm(forms.Form):
	arquivo = forms.FileField(label="Planilha InfoUSF", help_text="Envie um arquivo .xlsx com as colunas da planilha InfoUSF.")


@admin.register(EstabelecimentoSaude)
class EstabelecimentoSaudeAdmin(admin.ModelAdmin):
	change_list_template = "admin/EstabelecimentoSaude/change_list.html"
	change_form_template = "admin/EstabelecimentoSaude/change_form.html"
	list_display = ("nome", "cnes", "farmaceutico", "horario", "atualizado_em")
	search_fields = ("nome", "cnes", "gestor", "endereco", "email")
	list_filter = ("horario",)
	ordering = ("nome",)
	readonly_fields = ("criado_em", "atualizado_em")
	fieldsets = (
		("Identificacao", {"fields": ("cnes", "nome", "gestor")}),
		("Contato e endereco", {"fields": ("telefone", "email", "endereco", "link")}),
		("Funcionamento", {"fields": ("horario", "farmaceutico", "horario_farmaceutico", "competencias")}),
		("Localizacao", {"fields": ("latitude", "longitude")}),
		("Controle", {"fields": ("criado_em", "atualizado_em")}),
	)

	def get_urls(self):
		urls = super().get_urls()
		custom_urls = [
			path("upload-unidades/", self.admin_site.admin_view(self.upload_unidades), name="estabelecimentosaude_upload")
		]
		return custom_urls + urls

	def upload_unidades(self, request):
		if request.method == "POST":
			form = UploadUnidadesForm(request.POST, request.FILES)
			if form.is_valid():
				arquivo = form.cleaned_data["arquivo"]
				if not arquivo.name.lower().endswith((".xlsx", ".xls")):
					form.add_error("arquivo", "Envie um arquivo Excel .xls ou .xlsx.")
				else:
					try:
						resultado = importar_unidades(arquivo)
						self.message_user(
							request,
							f"Importação concluída: {resultado['criadas']} criadas, {resultado['atualizadas']} atualizadas e {resultado['ignoradas']} ignoradas.",
							messages.SUCCESS,
						)
						return redirect("..")
					except Exception as exc:
						form.add_error(None, str(exc))
		else:
			form = UploadUnidadesForm()

		context = {
			**self.admin_site.each_context(request),
			"title": "Importar unidades de saúde",
			"form": form,
			"opts": self.model._meta,
		}
		return render(request, "admin/EstabelecimentoSaude/upload_unidades.html", context)
