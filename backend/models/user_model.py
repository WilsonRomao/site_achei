from config import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    # Vamos usar JSON para armazenar uma lista simples ex: ["padrão", "prescritor"]
    perfis = db.Column(db.JSON, nullable=False, default=["padrão"])

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "perfis": self.perfis
        }

class SolicitacaoPerfil(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    perfil_solicitado = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pendente") # pendente, aprovado, recusado
    data_solicitacao = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    usuario = db.relationship('Usuario', backref='solicitacoes')

    def to_json(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "email_usuario": self.usuario.email if self.usuario else "",
            "perfil_solicitado": self.perfil_solicitado,
            "status": self.status,
            "data_solicitacao": self.data_solicitacao.strftime("%Y-%m-%d %H:%M:%S")
        }
