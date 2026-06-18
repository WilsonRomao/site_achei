from data_processing import limpeza_dos_dados
from models import Medicamento, EstabelecimentoSaude, Estoque
from config import db, app

def etl(fileName):
    df_limpo = limpeza_dos_dados(fileName)
    
    with app.app_context():
        # Dicionários de cache local em memória para evitar consultas de banco em excesso
        cache_estabelecimentos = {}
        cache_medicamentos = {}

        for _, row in df_limpo.iterrows():
            nome_estab = row['estabelecimento_saude']
            catmat_val = row['catmat']
            nome_med = row['medicamento']
            qtd = row['quantidade']

            # 1. Busca ou Cria Estabelecimento
            if nome_estab not in cache_estabelecimentos:
                estab = EstabelecimentoSaude.query.filter_by(nome=nome_estab).first()
                if not estab:
                    estab = EstabelecimentoSaude(nome=nome_estab)
                    db.session.add(estab)
                    db.session.flush() # Pega o ID sem commitar
                cache_estabelecimentos[nome_estab] = estab.id
            
            estab_id = cache_estabelecimentos[nome_estab]

            # 2. Busca ou Cria Medicamento
            if catmat_val not in cache_medicamentos:
                med = Medicamento.query.filter_by(catmat=catmat_val).first()
                if not med:
                    med = Medicamento(catmat=catmat_val, medicamento=nome_med)
                    db.session.add(med)
                cache_medicamentos[catmat_val] = True
            
            # 3. Busca ou Cria Estoque
            estoque_existente = Estoque.query.filter_by(
                medicamento_catmat=catmat_val, 
                estabelecimento_id=estab_id
            ).first()

            if estoque_existente:
                estoque_existente.quantidade = qtd
            else:
                novo_estoque = Estoque(
                    medicamento_catmat=catmat_val,
                    estabelecimento_id=estab_id,
                    quantidade=qtd
                )
                db.session.add(novo_estoque)
        
        db.session.commit()