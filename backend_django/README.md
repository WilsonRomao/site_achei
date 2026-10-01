# ACHEI - Backend Django

O backend oficial do ACHEI é uma API REST construída com Django REST Framework.

## Executar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

A API fica disponível em `http://localhost:8000/api/`.

## Principais rotas

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `GET /api/medicamentos/`
- `GET /api/estabelecimentos/`
- `GET /api/estoque/`
- `POST /api/uploads/`

Rotas administrativas e de upload exigem um token JWT no cabeçalho `Authorization`.