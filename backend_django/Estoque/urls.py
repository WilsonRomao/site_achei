from django.urls import path

from .views import EstoqueListView

urlpatterns = [
    path("", EstoqueListView.as_view(), name="estoque-list"),
]
