# contem as rotas e endpoints
from flask import request, jsonify
from config import app,db
from models import Medicamento
from pipeline import etl

import os

@app.route('/')
def index_page():
    return "<h1> Flask API </h1>"
@app.route('/medicamentos', methods=['GET'])
def listar_medicamentos():
    """
    Lista os estoques de medicamentos com paginação e filtros.
    ---
    tags:
      - Consulta Pública
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 20
      - name: q
        in: query
        type: string
        description: Busca por nome do medicamento
      - name: catmat
        in: query
        type: string
      - name: estabelecimento
        in: query
        type: string
    responses:
      200:
        description: Lista paginada de estoques
    """
    # 1. Captura parâmetros de paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int) # Itens por página

    # 2. Inicia a query base unindo as 3 tabelas
    from models import Estoque, EstabelecimentoSaude

    query = db.session.query(Estoque, Medicamento, EstabelecimentoSaude)\
        .join(Medicamento, Estoque.medicamento_catmat == Medicamento.catmat)\
        .join(EstabelecimentoSaude, Estoque.estabelecimento_id == EstabelecimentoSaude.id)

    # 3. Aplica os filtros dinâmicos
    catmat = request.args.get('catmat')
    estabelecimento = request.args.get('estabelecimento')
    q = request.args.get('q')

    if catmat:
        query = query.filter(Medicamento.catmat.ilike(f"%{catmat}%"))
    if estabelecimento:
        query = query.filter(EstabelecimentoSaude.nome.ilike(f"%{estabelecimento}%"))
    if q:
        query = query.filter(Medicamento.medicamento.ilike(f"%{q}%"))

    # 4. Aplica a PAGINAÇÃO no final da query filtrada
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # 5. Monta a resposta com metadados traduzindo pro formato antigo do React
    items = []
    for estoque_obj, med_obj, estab_obj in pagination.items:
        items.append({
            "catmat": med_obj.catmat,
            "medicamento": med_obj.medicamento,
            "quantidade": estoque_obj.quantidade,
            "estabelecimentoSaude": estab_obj.nome
        })

    return jsonify({
        "items": items,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev
    })

@app.route('/estabelecimentos', methods=['GET'])
def listar_estabelecimentos_unicas():
    """
    Retorna uma lista simples com o nome de todos os estabelecimentos.
    ---
    tags:
      - Consulta Pública
    responses:
      200:
        description: Lista de strings
    """
    from models import EstabelecimentoSaude
    estabelecimentos = EstabelecimentoSaude.query.order_by(EstabelecimentoSaude.nome).all()
    return jsonify([e.nome for e in estabelecimentos])

from controllers.auth import auth_bp
from controllers.admin import admin_bp
from flask_jwt_extended import jwt_required, get_jwt

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    """
    Faz o upload e processamento (ETL) da planilha do SUS.
    ---
    tags:
      - Administrador
    security:
      - Bearer: []
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Arquivo .xlsx de estoque
    responses:
      201:
        description: Arquivo processado com sucesso
      400:
        description: Arquivo inválido
      403:
        description: Acesso negado
    """
    claims = get_jwt()
    if "administrador" not in claims.get("perfis", []):
        return jsonify({"message": "Acesso negado. Apenas administradores podem fazer upload."}), 403

    # 1. Validação do arquivo
    if 'file' not in request.files:
        return jsonify({"message": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "Arquivo sem nome"}), 400

    try:
        # 2. Processa o arquivo em memória sem salvar em disco
        # Reseta o ponteiro pra ter certeza que está no início
        file.stream.seek(0)
        etl(fileName=file.stream) 

        # 3. Faz o upload do arquivo para o S3 (MinIO)
        file.stream.seek(0)
        from services.storage import upload_to_s3
        upload_to_s3(file.stream, file.filename)

        # 4. Retorno de sucesso para o React
        return jsonify({
            "message": "Arquivo processado e enviado para a nuvem com sucesso!"
        }), 201

    except Exception as e:
        print(f"Erro no pipeline ou upload: {e}")
        return jsonify({"message": f"Erro: {str(e)}"}), 500



#To run the aplication:
if __name__ == "__main__":
    import time
    from sqlalchemy.exc import OperationalError

    with app.app_context():
        # Aguarda o banco de dados subir antes de tentar criar as tabelas
        for i in range(15):
            try:
                db.create_all()
                print("Banco de dados conectado e tabelas criadas com sucesso!")
                
                # Semeando o Administrador inicial
                from models import Usuario
                if not Usuario.query.filter_by(email="admin@achei.com").first():
                    admin = Usuario(email="admin@achei.com", perfis=["administrador", "padrão"])
                    admin.set_senha("admin123")
                    db.session.add(admin)
                    db.session.commit()
                    print("Usuário Administrador inicial criado com sucesso.")
                    
                break
            except OperationalError:
                print(f"Banco de dados ainda não está pronto. Tentando novamente... ({i+1}/15)")
                time.sleep(2)

    app.run(debug=True, host='0.0.0.0', port=5000)


