from django.contrib import admin
from django.urls import path

from config.admin_csv import csv_download_response, render_csv_upload

from .importers import importar_estoque
from .models import Estoque


@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
	change_list_template = "admin/Estoque/change_list.html"
	list_display = ("medicamento", "estabelecimento", "quantidade")
	list_editable = ("quantidade",)
	list_filter = ("estabelecimento", "medicamento")
	search_fields = (
		"medicamento__catmat",
		"medicamento__medicamento",
		"estabelecimento__nome",
	)
	list_select_related = ("medicamento", "estabelecimento")

	def get_urls(self):
		urls = super().get_urls()
		custom_urls = [
			path("importar-csv/", self.admin_site.admin_view(self.importar_csv), name="estoque_importar_csv"),
			path("modelo-csv/", self.admin_site.admin_view(self.modelo_csv), name="estoque_modelo_csv"),
		]
		return custom_urls + urls

	def importar_csv(self, request):
		return render_csv_upload(
			self,
			request,
			"Importar estoque",
			"modelo-csv/",
			importar_estoque,
		)

	def modelo_csv(self, request):
		return csv_download_response(
			"modelo_estoque.csv",
			["catmat", "medicamento", "nome_estabelecimento", "quantidade"],
			["BR123456", "Paracetamol 500mg", "USF Centro", "25"],
		)
