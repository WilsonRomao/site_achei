import csv
import io

from django.db import transaction

from .models import Medicamento


@transaction.atomic
def importar_medicamentos(arquivo):
    texto = arquivo.read().decode("utf-8-sig")
    leitor = csv.DictReader(io.StringIO(texto))
    obrigatorias = {"catmat", "medicamento"}
    if not obrigatorias.issubset(leitor.fieldnames or []):
        raise ValueError("O CSV deve conter as colunas catmat e medicamento.")

    criados = 0
    atualizados = 0
    ignorados = 0
    for linha in leitor:
        catmat = (linha.get("catmat") or "").strip()
        nome = (linha.get("medicamento") or "").strip()
        if not catmat or not nome:
            ignorados += 1
            continue
        medicamento, criado = Medicamento.objects.update_or_create(
            catmat=catmat,
            defaults={"medicamento": nome},
        )
        if criado:
            criados += 1
        else:
            atualizados += 1

    return {"criados": criados, "atualizados": atualizados, "ignorados": ignorados}
