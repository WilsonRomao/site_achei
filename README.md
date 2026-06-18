# Site ACHEI - PET-SAÚDE DIGITAL (UFMS)

O projeto **ACHEI** é uma aplicação web moderna voltada para a gestão e exibição pública do estoque de medicamentos nas farmácias de unidades básicas de saúde (UBS) na cidade de Campo Grande, MS.

Este ecossistema foi desenhado com foco em **escalabilidade**, **segurança** e **usabilidade**. Ele é composto por uma arquitetura em microserviços (via Docker) separando claramente o Frontend, o Backend, o Banco de Dados e o Servidor de Arquivos (Storage S3).

---

## 🏛️ Arquitetura do Sistema

A infraestrutura completa roda de maneira local via `docker-compose`, espelhando perfeitamente um ambiente de nuvem de produção.

- **Frontend**: Aplicação SPA feita em **React** (via Vite), estilizada com **Bootstrap 5**. Responsável por entregar uma experiência limpa, fluida e responsiva para o usuário final.
- **Backend**: Servidor REST construído em **Flask** (Python). Gerencia a ingestão dos dados (ETL de planilhas de estoque), autenticação com tokens JWT e fornece as rotas de consumo para o Frontend.
- **Banco de Dados**: Utilizamos **PostgreSQL**, estruturado no modelo relacional 3FN (com tabelas de Medicamentos, Estabelecimentos e Estoques), garantindo integridade das informações.
- **Storage**: Para armazenar e versionar as planilhas do SUS (com milhares de linhas), acoplamos um servidor **MinIO**, que atua como um "Clone do Amazon S3", abstraindo o armazenamento local.

---

## 🚀 Como Executar o Projeto Localmente

O ambiente de desenvolvimento está contêinerizado. Para subir o projeto do zero, você precisará apenas do Docker e do Docker Compose instalados.

1. **Clone o Repositório**:
   Baixe o código para sua máquina.

2. **Configure as Variáveis de Ambiente**:
   Por questões de segurança, as senhas do banco e chaves de acesso não ficam salvas no repositório. Você precisa criar o seu próprio arquivo de configuração:
   - Na raiz do projeto, faça uma cópia do arquivo de exemplo:
     ```bash
     cp .env.example .env
     ```
   - Edite o arquivo `.env` gerado e coloque as senhas que preferir para o seu Banco de Dados e para o armazenamento do MinIO.

3. **Inicie os Containers**:
   Execute o seguinte comando na raiz do projeto:
   ```bash
   sudo docker compose up --build -d
   ```

4. **Portas da Aplicação**:
   - **Frontend (Interface do Usuário)**: [http://localhost:3000](http://localhost:3000)
   - **Backend (API)**: `http://localhost:5000`
   - **Banco (PostgreSQL)**: Porta interna `5432`
   - **MinIO Console**: `http://localhost:9001`

> 🔑 **Usuário Semente:** Ao inicializar a infraestrutura pela primeira vez, o Backend gera um usuário mestre com controle total. Use as credenciais `admin@achei.com` / `admin123` para acessar o Painel Administrativo de Usuários.

---

## 👥 Permissões e Perfis de Acesso (RBAC)

O ACHEI não possui apenas um cargo por pessoa. Cada usuário cadastrado possui uma **Lista de Perfis**, permitindo acúmulo de funções:
- **Padrão**: Criado automaticamente ao se cadastrar. Visualiza os medicamentos publicamente.
- **Prescritor**: Médicos, Enfermeiros e Odontologistas (Acesso reservado no menu).
- **Administrador**: Tem acesso ao Painel de Controle, aprova/recusa solicitações de acessos de outros usuários e faz upload da planilha mensal de estoques para atualizar o sistema.

Para informações mais aprofundadas sobre como codificar em cada ecossistema, consulte os sub-guias:
- ➡️ [Leia o README do Backend](./backend/README.md)
- ➡️ [Leia o README do Frontend](./frontend/README.md)

---

## 🛠️ Padrões de Contribuição (GitHub Flow)

1. **Branching**: Crie sempre uma nova branch a partir da `main` para desenvolver sua feature ou correção (ex: `feature/nova-pagina-estoque`).
2. **Commits (Conventional Commits)**:
   - `feat`: Uma nova funcionalidade (ex: `feat: adiciona filtro de UBS`).
   - `fix`: Correção de bug (ex: `fix: corrige paginação`).
   - `docs`: Mudanças em documentação.
   - `chore`: Atualização de pacotes/configs.
3. **Pull Request (PR)**: Finalizado o escopo, abra um PR para a `main`.
