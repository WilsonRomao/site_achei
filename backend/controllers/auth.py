from flask import Blueprint, request, jsonify
from models import Usuario, SolicitacaoPerfil
from config import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registra um novo usuário no sistema.
    ---
    tags:
      - Autenticação
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: usuario@teste.com
            senha:
              type: string
              example: senha123
    responses:
      201:
        description: Usuário cadastrado com sucesso
      400:
        description: Erro de validação
    """
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({"message": "Email e senha são obrigatórios"}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"message": "Email já cadastrado"}), 400

    # Todos começam como padrão, a escolha via interface é ignorada.
    novo_usuario = Usuario(email=email, perfis=["padrão"])
    novo_usuario.set_senha(senha)
    
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Realiza o login e retorna o Token JWT.
    ---
    tags:
      - Autenticação
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: admin@achei.com
            senha:
              type: string
              example: admin123
    responses:
      200:
        description: Login realizado com sucesso
      401:
        description: Credenciais inválidas
    """
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not usuario.check_senha(senha):
        return jsonify({"message": "Credenciais inválidas"}), 401

    # Cria o token injetando os dados de perfil
    access_token = create_access_token(
        identity=str(usuario.id), 
        additional_claims={"perfis": usuario.perfis, "email": usuario.email}
    )
    
    return jsonify({
        "token": access_token,
        "usuario": usuario.to_json()
    }), 200

@auth_bp.route('/solicitar', methods=['POST'])
@jwt_required()
def solicitar_perfil():
    """
    Solicita a elevação de privilégio (novo perfil).
    ---
    tags:
      - Autenticação
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            perfil:
              type: string
              example: prescritor
    responses:
      201:
        description: Solicitação enviada com sucesso
      400:
        description: Perfil inválido ou solicitação pendente
    """
    data = request.get_json()
    perfil_desejado = data.get('perfil')
    usuario_id = int(get_jwt_identity())

    if perfil_desejado not in ['administrador', 'prescritor']:
        return jsonify({"message": "Perfil inválido"}), 400

    # Verifica se já existe uma solicitação pendente
    existente = SolicitacaoPerfil.query.filter_by(usuario_id=usuario_id, perfil_solicitado=perfil_desejado, status="pendente").first()
    if existente:
        return jsonify({"message": "Você já possui uma solicitação pendente para este perfil."}), 400
    
    nova_solicitacao = SolicitacaoPerfil(usuario_id=usuario_id, perfil_solicitado=perfil_desejado)
    db.session.add(nova_solicitacao)
    db.session.commit()

    return jsonify({"message": "Solicitação enviada com sucesso!"}), 201
