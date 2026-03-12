import os
import pandas as pd
from sqlalchemy import create_engine
from config import app ,db
from processamento import processar_r84


def etl(fileName):
    #____EXTRAÇÃO E TRANSFORMAÇÃO___________________________
    medicamentos = processar_r84(fileName)

    #____CARREGA AS INFORMAÇÕES NO BANCO DE DADOS____________

    # Configuração da conexão
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    try:
        medicamentos.to_sql('medicamento', con=db.engine, if_exists='replace', index=False)
        print("Pipeline finalizado: Dados inseridos no banco.")
    except Exception as e:
        print(f"Erro ao inserir no banco: {e}")
        raise e # Relança o erro para o Flask capturar no bloco try/except dele


    # print(medicamentos_df)

    #__Salva os dados no bd







