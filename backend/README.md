# ACHEI - Backend (API)

O Backend do projeto ACHEI é o cérebro da operação. Ele é uma API REST construída em **Python + Flask**, projetada para lidar com processos pesados (como análise e normalização de planilhas de estoque com mais de 30 mil linhas) de forma rápida e segura.

## 🛠️ Tecnologias Principais

- **Flask**: Microframework para construção ágil das rotas.
- **SQLAlchemy (PostgreSQL)**: ORM poderoso que conversa nativamente com nosso banco PostgreSQL, mapeando nossas tabelas de `Usuario`, `Medicamento`, `EstabelecimentoSaude` e `Estoque`.
- **Flask-JWT-Extended**: Sistema avançado de autenticação via *JSON Web Tokens*. Nós injetamos a lista de `perfis` do usuário diretamente no payload do token para controle de rotas sem precisar consultar o banco a cada requisição.
- **Boto3 (S3/MinIO)**: Usado para upload "na nuvem" das planilhas brutas. Permite que o projeto não perca as planilhas antigas cada vez que o servidor for reiniciado.
- **Pandas**: Motor analítico utilizado na ingestão do arquivo (pipeline.py) que limpa, desduplica e quebra a tabela enorme do Excel em sub-estruturas relacionais (3FN).

## 📂 Estrutura de Diretórios

- `/controllers/`: Rotas da aplicação (ex: `auth.py`, `admin.py`, `main.py`).
- `/models/`: Classes do SQLAlchemy que espelham o Banco de Dados.
- `pipeline.py`: Script de ETL. Puxa a planilha recém-enviada pelo Admin para o S3, limpa valores vazios, registra Estabelecimentos e Medicamentos independentes e consolida o saldo no Estoque.
- `config.py`: Conecta com variáveis de ambiente (DB URL, Chaves JWT e S3).

## 🚨 Executando o Pipeline

O usuário Administrador faz o upload da planilha (via Frontend).
1. A rota `/upload` intercepta a chamada.
2. Salva o `.xlsx` fisicamente em nosso servidor **MinIO (Bucket S3)**.
3. Chama a função `limpeza_dos_dados()` do `pipeline.py`.
4. O *Pandas* mastiga os dados e populariza as 3 tabelas no **PostgreSQL** de forma relacional.
