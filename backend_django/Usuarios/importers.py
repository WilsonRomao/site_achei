import csv
import io
import json

from django.db import transaction

from .models import Usuario


def _booleano(valor, padrao=False):
    texto = (valor or "").strip().lower()
    if not texto:
        return padrao
    return texto in {"1", "true", "sim", "s", "yes", "y"}


@transaction.atomic
def importar_usuarios(arquivo):
    texto = arquivo.read().decode("utf-8-sig")
    leitor = csv.DictReader(io.StringIO(texto))
    obrigatorias = {"email", "senha", "perfis", "is_staff", "is_active"}
    if not obrigatorias.issubset(leitor.fieldnames or []):
        raise ValueError("O CSV deve conter email, senha, perfis, is_staff e is_active.")

    criados = 0
    atualizados = 0
    ignorados = 0
    for linha in leitor:
        email = (linha.get("email") or "").strip().lower()
        senha = (linha.get("senha") or "").strip()
        if not email:
            ignorados += 1
            continue
        if not senha and not Usuario.objects.filter(email=email).exists():
            raise ValueError(f"A senha é obrigatória para o novo usuário {email}.")

        perfis_texto = (linha.get("perfis") or "padrão").strip()
        try:
            perfis = json.loads(perfis_texto) if perfis_texto.startswith("[") else [item.strip() for item in perfis_texto.split("|") if item.strip()]
        except json.JSONDecodeError as exc:
            raise ValueError(f"Perfis inválidos para {email}.") from exc

        usuario = Usuario.objects.filter(email=email).first()
        criado = usuario is None
        if criado:
            usuario = Usuario(email=email)
        usuario.perfis = perfis or ["padrão"]
        usuario.is_staff = _booleano(linha.get("is_staff"))
        if criado:
            usuario.is_superuser = False
        usuario.is_active = _booleano(linha.get("is_active"), True)
        if senha:
            usuario.set_password(senha)
        usuario.save()
        if criado:
            criados += 1
        else:
            atualizados += 1

    return {"criados": criados, "atualizados": atualizados, "ignorados": ignorados}
