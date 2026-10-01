import re
import unicodedata

import pandas as pd
from django.db import transaction

from .models import EstabelecimentoSaude


def _normalizar_coluna(valor):
    texto = unicodedata.normalize("NFKD", str(valor or ""))
    texto = texto.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]", "", texto)


def _texto(valor):
    if pd.isna(valor):
        return ""
    return str(valor).strip()


def _coordenada(valor):
    texto = _texto(valor).replace(",", ".")
    if not texto:
        return None
    numero = float(texto)
    if abs(numero) > 90:
        numero /= 1_000_000
    return numero


def _cnes(valor):
    texto = _texto(valor)
    if not texto:
        return None
    if texto.endswith(".0"):
        texto = texto[:-2]
    return texto


@transaction.atomic
def importar_unidades(arquivo):
    df = pd.read_excel(arquivo)
    if df.empty:
        raise ValueError("A planilha está vazia.")

    colunas = {_normalizar_coluna(coluna): coluna for coluna in df.columns}
    obrigatorias = {"nome": "nome"}
    ausentes = [rotulo for chave, rotulo in obrigatorias.items() if chave not in colunas]
    if ausentes:
        raise ValueError("Coluna obrigatória ausente: nome.")

    def coluna(chave):
        return colunas.get(_normalizar_coluna(chave))

    criadas = 0
    atualizadas = 0
    ignoradas = 0

    for _, linha in df.iterrows():
        nome = _texto(linha.get(coluna("nome")))
        if not nome:
            ignoradas += 1
            continue

        cnes = _cnes(linha.get(coluna("CNES"))) if coluna("CNES") else None
        dados = {
            "nome": nome,
            "cnes": cnes,
            "latitude": _coordenada(linha.get(coluna("latitude"))) if coluna("latitude") else None,
            "longitude": _coordenada(linha.get(coluna("longitude"))) if coluna("longitude") else None,
            "horario": _texto(linha.get(coluna("horarioFuncionamento"))) if coluna("horarioFuncionamento") else None,
            "farmaceutico": _texto(linha.get(coluna("farmaceutico"))).upper() in {"SIM", "S", "TRUE", "1"} if coluna("farmaceutico") else False,
            "horario_farmaceutico": _texto(linha.get(coluna("horarioFarmaceutico"))) if coluna("horarioFarmaceutico") else None,
            "link": _texto(linha.get(coluna("link"))) or None if coluna("link") else None,
        }

        unidade = None
        if cnes:
            unidade = EstabelecimentoSaude.objects.filter(cnes=cnes).first()
        if unidade is None:
            unidade = EstabelecimentoSaude.objects.filter(nome=nome).first()

        if unidade is None:
            EstabelecimentoSaude.objects.create(**dados)
            criadas += 1
        else:
            for campo, valor in dados.items():
                setattr(unidade, campo, valor)
            unidade.save()
            atualizadas += 1

    return {"criadas": criadas, "atualizadas": atualizadas, "ignoradas": ignoradas}