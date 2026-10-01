from django.urls import path

from .views import (
    AdminSolicitacaoActionView,
    AdminSolicitacaoListView,
    AdminUserListCreateView,
    AdminUserPerfilUpdateView,
    LoginView,
    RegisterView,
    SolicitarPerfilView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/solicitar/", SolicitarPerfilView.as_view(), name="solicitar-perfil"),
    path("admin/usuarios", AdminUserListCreateView.as_view(), name="admin-usuarios"),
    path("admin/usuarios/<int:pk>/perfis", AdminUserPerfilUpdateView.as_view(), name="admin-usuario-perfis"),
    path("admin/solicitacoes", AdminSolicitacaoListView.as_view(), name="admin-solicitacoes"),
    path("admin/solicitacoes/<int:pk>/<str:acao>", AdminSolicitacaoActionView.as_view(), name="admin-solicitacao-action"),
]
