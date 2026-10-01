from django.urls import path

from .views import MedicamentoListView

urlpatterns = [
    path("", MedicamentoListView.as_view(), name="medicamentos-list"),
]
