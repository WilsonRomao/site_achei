from django.contrib import admin
from django.urls import path

from config.admin_csv import csv_download_response, render_csv_upload

from .models import Medicamento
from .importers import importar_medicamentos


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
	change_list_template = "admin/Medicamento/change_list.html"
	list_display = ("catmat", "medicamento")
	search_fields = ("catmat", "medicamento")
	ordering = ("medicamento",)

	def get_urls(self):
		urls = super().get_urls()
		custom_urls = [
			path("importar-csv/", self.admin_site.admin_view(self.importar_csv), name="medicamento_importar_csv"),
			path("modelo-csv/", self.admin_site.admin_view(self.modelo_csv), name="medicamento_modelo_csv"),
		]
		return custom_urls + urls

	def importar_csv(self, request):
		return render_csv_upload(
			self,
			request,
			"Importar medicamentos",
			"modelo-csv/",
			importar_medicamentos,
		)

	def modelo_csv(self, request):
		return csv_download_response(
			"modelo_medicamentos.csv",
			["catmat", "medicamento"],
			["BR123456", "Paracetamol 500mg"],
		)
