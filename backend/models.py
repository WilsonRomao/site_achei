# contem os modelos de banco de dados

from config import db

class Medicamento(db.Model):
    catmat = db.Column(db.String(50), primary_key=True)
    medicamento = db.Column(db.String(100), unique = False, nullable = False)
    quantidade = db.Column(db.Integer, unique=False, nullable = False)
    estabelecimento_saude = db.Column(db.String(200), unique=False, nullable = False)

    def to_json(self):
        return {
            "catmat" : self.catmat,
            "medicamento" : self.medicamento,
            "quantidade" : self.quantidade,
            "estabelecimentoSaude": self.estabelecimento_saude
        }

