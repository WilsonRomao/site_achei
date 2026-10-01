from rest_framework import serializers

from .models import SolicitacaoPerfil, Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "email", "perfis"]
        read_only_fields = ["id", "perfis"]


class UsuarioAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "email", "perfis"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=False)
    senha = serializers.CharField(write_only=True, min_length=8, required=False)

    class Meta:
        model = Usuario
        fields = ["email", "password", "senha"]

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email já cadastrado.")
        return value

    def validate(self, attrs):
        if not attrs.get("password") and not attrs.get("senha"):
            raise serializers.ValidationError({"password": "Informe uma senha."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password", None) or validated_data.pop("senha")
        user = Usuario(**validated_data)
        user.set_password(password)
        user.perfis = ["padrão"]
        user.save()
        return user


class SolicitacaoPerfilSerializer(serializers.ModelSerializer):
    usuario_email = serializers.SerializerMethodField()

    class Meta:
        model = SolicitacaoPerfil
        fields = ["id", "usuario", "usuario_email", "perfil_solicitado", "status", "data_solicitacao"]

    def get_usuario_email(self, obj):
        return obj.usuario.email
