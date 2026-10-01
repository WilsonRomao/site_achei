from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import SolicitacaoPerfil, Usuario
from .permissions import IsAdministrador
from .serializers import (
    RegisterSerializer,
    SolicitacaoPerfilSerializer,
    UsuarioAdminSerializer,
    UsuarioSerializer,
)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Usuário cadastrado com sucesso!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("senha")

        if not email or not password:
            return Response(
                {"message": "Email e senha são obrigatórios"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = Usuario.objects.filter(email=email).first()
        if user is None or not user.is_active or not user.check_password(password):
            return Response(
                {"message": "Credenciais inválidas"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response(
            {
                "token": access_token,
                "usuario": UsuarioSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class SolicitarPerfilView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        perfil = request.data.get("perfil")
        if perfil not in ["administrador", "prescritor"]:
            return Response({"message": "Perfil inválido"}, status=status.HTTP_400_BAD_REQUEST)

        if SolicitacaoPerfil.objects.filter(
            usuario=request.user,
            perfil_solicitado=perfil,
            status="pendente",
        ).exists():
            return Response(
                {"message": "Você já possui uma solicitação pendente para este perfil."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        SolicitacaoPerfil.objects.create(usuario=request.user, perfil_solicitado=perfil)
        return Response({"message": "Solicitação enviada com sucesso!"}, status=status.HTTP_201_CREATED)


class AdminUserListCreateView(APIView):
    permission_classes = [IsAdministrador]

    def get(self, request, *args, **kwargs):
        usuarios = Usuario.objects.all().order_by("email")
        serializer = UsuarioAdminSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        usuario = serializer.save()
        if request.data.get("perfis"):
            usuario.perfis = request.data.get("perfis")
            usuario.save(update_fields=["perfis"])

        return Response({"message": "Usuário criado com sucesso."}, status=status.HTTP_201_CREATED)


class AdminUserPerfilUpdateView(APIView):
    permission_classes = [IsAdministrador]

    def put(self, request, pk, *args, **kwargs):
        try:
            usuario = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return Response({"message": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        perfis = request.data.get("perfis", usuario.perfis or [])
        usuario.perfis = perfis
        usuario.save(update_fields=["perfis"])
        return Response({"message": "Perfis atualizados com sucesso."}, status=status.HTTP_200_OK)


class AdminSolicitacaoListView(APIView):
    permission_classes = [IsAdministrador]

    def get(self, request, *args, **kwargs):
        solicitacoes = SolicitacaoPerfil.objects.select_related("usuario").order_by("-data_solicitacao")
        serializer = SolicitacaoPerfilSerializer(solicitacoes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminSolicitacaoActionView(APIView):
    permission_classes = [IsAdministrador]

    def post(self, request, pk, acao, *args, **kwargs):
        if acao not in ["aprovar", "recusar"]:
            return Response({"message": "Ação inválida."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            solicitacao = SolicitacaoPerfil.objects.get(pk=pk)
        except SolicitacaoPerfil.DoesNotExist:
            return Response({"message": "Solicitação não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        if acao == "aprovar":
            solicitacao.status = "aprovado"
            perfis = list(solicitacao.usuario.perfis or [])
            if solicitacao.perfil_solicitado not in perfis:
                perfis.append(solicitacao.perfil_solicitado)
            solicitacao.usuario.perfis = perfis
            solicitacao.usuario.save(update_fields=["perfis"])
        else:
            solicitacao.status = "recusado"

        solicitacao.save(update_fields=["status"])
        return Response({"message": f"Solicitação {acao}da com sucesso."}, status=status.HTTP_200_OK)
