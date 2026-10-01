from django.urls import path

from .views import EstabelecimentoListView

urlpatterns = [
    path("", EstabelecimentoListView.as_view(), name="estabelecimentos-list"),
]
