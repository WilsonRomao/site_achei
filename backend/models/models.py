from config import db

class EstabelecimentoSaude(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.Text, unique=True, nullable=False)

    # Relacionamento (opcional, facilita buscas reversas se necessário)
    estoques = db.relationship('Estoque', backref='estabelecimento', lazy=True)

class Medicamento(db.Model):
    catmat = db.Column(db.String(50), primary_key=True)
    medicamento = db.Column(db.Text, nullable=False)

    # Relacionamento
    estoques = db.relationship('Estoque', backref='medicamento_rel', lazy=True)

class Estoque(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    
    medicamento_catmat = db.Column(db.String(50), db.ForeignKey('medicamento.catmat'), nullable=False)
    estabelecimento_id = db.Column(db.Integer, db.ForeignKey('estabelecimento_saude.id'), nullable=False)

    # Impede que o mesmo medicamento seja cadastrado duas vezes no mesmo posto (deve ser somado/atualizado)
    __table_args__ = (
        db.UniqueConstraint('medicamento_catmat', 'estabelecimento_id', name='_medicamento_estabelecimento_uc'),
    )
