# contem as rotas e endpoints
from flask import request, jsonify
from werkzeug.utils import secure_filename
from config import app,db
from models import Medicamento
from pipeline import etl

import os


@app.route('/medicamentos', methods=['GET'])
def listar_medicamentos():
    # 1. Captura parâmetros de paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int) # Itens por página

    # 2. Inicia a query base
    query = Medicamento.query

    # 3. Aplica os filtros dinâmicos (Catmat, estabelecimento, Busca)
    catmat = request.args.get('catmat')
    estabelecimento = request.args.get('estabelecimento')
    q = request.args.get('q')

    if catmat:
        query = query.filter(Medicamento.catmat.ilike(f"%{catmat}%"))
    if estabelecimento:
        query = query.filter(Medicamento.estabelecimento_saude.ilike(f"%{estabelecimento}%"))
    if q:
        query = query.filter(Medicamento.medicamento.ilike(f"%{q}%"))

    # 4. Aplica a PAGINAÇÃO no final da query filtrada
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # 5. Monta a resposta com metadados
    return jsonify({
        "items": [m.to_json() for m in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev
    })

@app.route('/estabelecimentos', methods=['GET'])
def listar_estabelecimentos_unicas():
    # Busca apenas a coluna 'estabelecimento', remove duplicatas e ordena
    estabelecimentos = db.session.query(Medicamento.estabelecimento_saude).distinct().order_by(Medicamento.estabelecimento_saude).all()
    # Retorna uma lista simples: ["UBS Centro", "Hospital Norte", ...]
    return jsonify([u[0] for u in estabelecimentos if u[0]])

@app.route("/upload", methods=["POST"])
def upload():
    # 1. Validação básica: verifica se o ficheiro existe na requisição
    if 'file' not in request.files:
        return jsonify({"message": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"message": "Arquivo sem nome"}), 400

    # 2. Configuração de caminhos e segurança
    upload_path ="uploads"
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    # Limpa o nome do ficheiro para evitar ataques de Path Traversal
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_path, filename)
    
    try:
        # 3. Salva o ficheiro temporariamente
        file.save(file_path)

        # 4. Aciona o Pipeline de ETL
        # O ETL vai ler o ficheiro, limpar os dados e persistir no Banco
        etl(fileName=file_path) 

        # 5. Limpeza de disco: Remove o ficheiro após o processamento
        if os.path.exists(file_path):
            os.remove(file_path)

        return jsonify({
            "message": "Arquivo processado e dados atualizados no banco com sucesso!",
            "status": "success"
        }), 201

    except Exception as e:
        # Se algo falhar no processamento ou no banco, garante que o erro chegue ao React
        print(f"Erro no pipeline: {str(e)}")
        
        # # Tenta remover o ficheiro mesmo em caso de erro para não poluir o servidor
        # if os.path.exists(file_path):
        #     os.remove(file_path)
            
        return jsonify({
            "message": f"Erro interno no processamento: {str(e)}",
            "status": "error"
        }), 500



#To run the aplication:
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)


