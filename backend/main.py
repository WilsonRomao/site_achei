# contem as rotas e endpoints
from flask import request, jsonify
from config import app,db
from models import Medicamento
from pipeline import etl

import os

@app.route("/medicamento", methods=["GET"])
def get_medicamento():
    medicamento = Medicamento.query.all()
    json_medicamento = list(map(lambda x: x.to_json(), medicamento))
    return jsonify({"Medicamento":json_medicamento})


@app.route("/upload", methods=["POST"])
def upload():
    # 1. Validação do arquivo
    if 'file' not in request.files:
        return jsonify({"message": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "Arquivo sem nome"}), 400

    # 2. Caminhos (backend/uploads)
    upload_path = os.path.join("uploads")
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    file_path = os.path.join(upload_path, file.filename)
    file.save(file_path)

    try:
        # 3. O Pipeline aciona o Banco de Dados
        # Passe o caminho completo do arquivo para o seu processador
        etl(fileName=file_path) 

        # 4. Retorno de sucesso para o React
        # O React receberá esse 201 e saberá que os dados já estão no banco
        return jsonify({
            "message": "Arquivo processado e dados salvos no banco com sucesso!"
        }), 201

    except Exception as e:
        # Se o banco de dados falhar, o erro cai aqui
        print(f"Erro no pipeline: {e}")
        return jsonify({"message": f"Erro ao salvar no banco: {str(e)}"}), 500



#To run the aplication:
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)


