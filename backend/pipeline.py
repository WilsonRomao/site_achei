from processamento_2 import limpeza_dos_dados
from models import Medicamento
from config import db, app

def etl(fileName):
    # 1. Extração e Limpeza
    df_limpo = limpeza_dos_dados(fileName)
    
        # 2. Carga no Banco de Dados
    
    with app.app_context():
        try:
            for _, row in df_limpo.iterrows():
                # Busca pelo par da Chave Primária Composta
                existente = Medicamento.query.get((row['estabelecimento_saude'],row['catmat']))

                if existente:
                    # Atualiza apenas se a quantidade mudou (opcional, para ganho de performance)
                    existente.quantidade = row['quantidade']
                    existente.medicamento = row['medicamento']
                else:
                    novo = Medicamento(
                        estabelecimento_saude=row['estabelecimento_saude'],
                        catmat=row['catmat'],
                        medicamento=row['medicamento'],
                        quantidade=row['quantidade']                      
                    )
                    db.session.add(novo)
            
            # Commit único após processar todo o arquivo (muito mais rápido)
            db.session.commit()
            print(f"Sucesso: {fileName} processado e salvo.")
            
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar no banco: {e}")
            raise e