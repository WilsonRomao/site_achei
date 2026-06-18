from flask import Blueprint, request, jsonify
from models import Usuario, SolicitacaoPerfil
from config import db
from flask_jwt_extended import jwt_required, get_jwt

admin_bp = Blueprint('admin', __name__)

def admin_required():
    claims = get_jwt()
    if "administrador" not in claims.get("perfis", []):
        return False
    return True

@admin_bp.route('/usuarios', methods=['GET'])
@jwt_required()
def listar_usuarios():
    """
    Lista todos os usuários cadastrados.
    ---
    tags:
      - Administrador
    security:
      - Bearer: []
    responses:
      200:
        description: Lista de usuários
      403:
        description: Acesso negado
    """
    if not admin_required(): return jsonify({"message": "Acesso negado"}), 403
    usuarios = Usuario.query.all()
    return jsonify([u.to_json() for u in usuarios])

@admin_bp.route('/usuarios', methods=['POST'])
@jwt_required()
def criar_usuario():
    """
    Cria proativamente um novo usuário no sistema.
    ---
    tags:
      - Administrador
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            senha:
              type: string
            perfis:
              type: array
              items:
                type: string
    responses:
      201:
        description: Usuário criado com sucesso
      400:
        description: Usuário já existe
    """
    if not admin_required(): return jsonify({"message": "Acesso negado"}), 403
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    perfis = data.get('perfis', ["padrão"])

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"message": "Usuário já existe"}), 400
    
    novo = Usuario(email=email, perfis=perfis)
    novo.set_senha(senha)
    db.session.add(novo)
    db.session.commit()
    return jsonify(novo.to_json()), 201

@admin_bp.route('/usuarios/<int:id>/perfis', methods=['PUT'])
@jwt_required()
def atualizar_perfis(id):
    """
    Atualiza a lista de perfis de um usuário.
    ---
    tags:
      - Administrador
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            perfis:
              type: array
              items:
                type: string
    responses:
      200:
        description: Perfis atualizados com sucesso
      403:
        description: Acesso negado
    """
    if not admin_required(): return jsonify({"message": "Acesso negado"}), 403
    usuario = Usuario.query.get_or_404(id)
    data = request.get_json()
    
    # Previne que o administrador principal remova seu próprio acesso admin
    if usuario.email == "admin@achei.com" and "administrador" not in data.get('perfis', []):
        return jsonify({"message": "Não é possível remover o perfil administrador do usuário raiz."}), 400

    usuario.perfis = data.get('perfis', ["padrão"])
    db.session.commit()
    return jsonify(usuario.to_json())

@admin_bp.route('/solicitacoes', methods=['GET'])
@jwt_required()
def listar_solicitacoes():
    """
    Lista todas as solicitações de acesso pendentes e resolvidas.
    ---
    tags:
      - Administrador
    security:
      - Bearer: []
    responses:
      200:
        description: Lista de solicitações
    """
    if not admin_required(): return jsonify({"message": "Acesso negado"}), 403
    solicitacoes = SolicitacaoPerfil.query.order_by(SolicitacaoPerfil.data_solicitacao.desc()).all()
    return jsonify([s.to_json() for s in solicitacoes])

@admin_bp.route('/solicitacoes/<int:id>/<acao>', methods=['POST'])
@jwt_required()
def processar_solicitacao(id, acao):
    """
    Aprova ou recusa a solicitação de perfil de um usuário.
    ---
    tags:
      - Administrador
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: acao
        in: path
        type: string
        enum: [aprovar, recusar]
        required: true
    responses:
      200:
        description: Solicitação processada com sucesso
      400:
        description: Solicitação já processada ou ação inválida
    """
    if not admin_required(): return jsonify({"message": "Acesso negado"}), 403
    
    solicitacao = SolicitacaoPerfil.query.get_or_404(id)
    if solicitacao.status != "pendente":
        return jsonify({"message": "Solicitação já foi processada"}), 400
    
    if acao == "aprovar":
        solicitacao.status = "aprovado"
        usuario = solicitacao.usuario
        # Adiciona o perfil se já não existir
        perfis_atuais = usuario.perfis
        if solicitacao.perfil_solicitado not in perfis_atuais:
            novo_perfis = list(perfis_atuais)
            novo_perfis.append(solicitacao.perfil_solicitado)
            usuario.perfis = novo_perfis
    elif acao == "recusar":
        solicitacao.status = "recusado"
    else:
        return jsonify({"message": "Ação inválida"}), 400

    db.session.commit()
    return jsonify(solicitacao.to_json())
