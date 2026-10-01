import csv
import io

from django.db import transaction

from EstabelecimentoSaude.models import EstabelecimentoSaude
from Medicamento.models import Medicamento

from .models import Estoque


@transaction.atomic
def importar_estoque(arquivo):
    texto = arquivo.read().decode("utf-8-sig")
    leitor = csv.DictReader(io.StringIO(texto))
    obrigatorias = {"catmat", "medicamento", "nome_estabelecimento", "quantidade"}
    if not obrigatorias.issubset(leitor.fieldnames or []):
        raise ValueError("O CSV deve conter catmat, medicamento, nome_estabelecimento e quantidade.")

    criados = 0
    atualizados = 0
    ignorados = 0
    for linha in leitor:
        catmat = (linha.get("catmat") or "").strip()
        nome_medicamento = (linha.get("medicamento") or "").strip()
        nome_unidade = (linha.get("nome_estabelecimento") or "").strip()
        quantidade_texto = (linha.get("quantidade") or "").strip()
        if not catmat or not nome_medicamento or not nome_unidade:
            ignorados += 1
            continue
        try:
            quantidade = int(quantidade_texto)
        except ValueError as exc:
            raise ValueError(f"Quantidade inválida para {catmat}: {quantidade_texto}") from exc
        if quantidade < 0:
            raise ValueError(f"Quantidade não pode ser negativa para {catmat}.")

        medicamento, _ = Medicamento.objects.update_or_create(
            catmat=catmat,
            defaults={"medicamento": nome_medicamento},
        )
        estabelecimento, _ = EstabelecimentoSaude.objects.get_or_create(nome=nome_unidade)
        _, criado = Estoque.objects.update_or_create(
            medicamento=medicamento,
            estabelecimento=estabelecimento,
            defaults={"quantidade": quantidade},
        )
        if criado:
            criados += 1
        else:
            atualizados += 1

    return {"criados": criados, "atualizados": atualizados, "ignorados": ignorados}
