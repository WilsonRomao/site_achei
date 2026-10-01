# Backlog de Issues - ACHEI

Este documento consolida as issues do projeto com base no documento de requisitos do sistema ACHEI, incluindo as prioridades de negócio, casos de uso, requisitos funcionais e não funcionais.

---

## Milestone 1 - Fundação e migração

### Issue 1 - Feature: Migrar o backend Flask para Django mantendo compatibilidade com o frontend

**Tipo:** feature  
**Prioridade:** Alta

**Descrição**  
O projeto foi inicialmente desenvolvido em Flask, mas a base do Django já foi iniciada. Esta issue tem como objetivo migrar o backend para Django, preservando o contrato atual da API consumida pelo frontend e reduzindo a dependência do Flask como backend principal.

**Objetivo**
- Tornar o Django o backend principal do sistema
- Preservar os endpoints e payloads consumidos pelo frontend
- Remover dependência ativa do Flask no ambiente de execução

**Requisitos cobertos**
- Base da arquitetura do projeto
- Migração do backend
- Compatibilidade com o frontend
- Sustentação da solução em produção

**Critérios de aceite**
- [ ] O Django passa a ser o backend principal do projeto
- [ ] A API se mantém compatível com o frontend atual
- [ ] Os endpoints principais continuam funcionais
- [ ] A configuração do ambiente e dependências foi documentada
- [ ] O projeto não depende mais do Flask para execução normal

**Labels**
- `backend`  
- `django`  
- `migration`  
- `priority-high`

---

### Issue 2 - Fix: Corrigir a base Django e o ambiente para execução estável

**Tipo:** fix  
**Prioridade:** Alta

**Descrição**  
A estrutura Django foi iniciada, mas ainda há inconsistências de ambiente, dependências e configuração que impedem a migração completa e a execução estável do projeto.

**Objetivo**
- Ajustar a configuração do ambiente Python
- Corrigir dependências e arquivos de configuração
- Garantir que o projeto Django execute corretamente

**Requisitos cobertos**
- Configuração do ambiente de desenvolvimento
- Arquivos de dependência
- Execução estável da aplicação

**Critérios de aceite**
- [ ] O ambiente Python do projeto está corretamente configurado
- [ ] As dependências do Django são instaláveis e consistentes
- [ ] A configuração do projeto não apresenta erros na inicialização
- [ ] O backend Django consegue ser executado localmente
- [ ] O processo de configuração está documentado

**Labels**
- `backend`  
- `django`  
- `fix`  
- `environment`  
- `priority-high`

---

## Milestone 2 - Autenticação e autorização

### Issue 3 - Feature: Implementar autenticação JWT e RBAC no Django

**Tipo:** feature  
**Prioridade:** Alta

**Descrição**  
O sistema precisa manter autenticação por email e senha, geração de token JWT e controle de acessos por perfil. A lógica atual do Flask usa perfis embutidos nos tokens para autorização de áreas administrativas e públicas.

**Objetivo**
- Permitir cadastro e login
- Gerar JWT com informações do usuário
- Restrigir acesso conforme o perfil
- Manter segurança e integridade do sistema

**Requisitos cobertos**
- RF07 — restringir acesso administrativo
- RNF03 — garantir controle de acesso
- Classes de usuário do documento
- UC de autenticação e autorização

**Critérios de aceite**
- [ ] Usuário consegue se cadastrar
- [ ] Usuário consegue logar com email e senha
- [ ] O sistema retorna token JWT no login
- [ ] Perfis do usuário são transmitidos no token
- [ ] Usuários comuns não acessam áreas administrativas
- [ ] Administradores gerenciam permissões e usuários
- [ ] A API retorna erros de autenticação claros

**Labels**
- `backend`  
- `authentication`  
- `rbac`  
- `priority-high`

---

### Issue 4 - Feature: Implementar controle de perfis e autorização administrativa

**Tipo:** feature  
**Prioridade:** Alta

**Descrição**  
As permissões do sistema devem seguir a estrutura definida no documento: usuário, prescritor e administrador. Essa funcionalidade garante que ações sensíveis sejam acessíveis apenas para usuários autorizados.

**Objetivo**
- Diferenciar perfis de usuário
- Controlar ações administrativas
- Validar permissões sobre endpoints e telas

**Critérios de aceite**
- [ ] Usuário comum não acessa painel administrativo
- [ ] Prescritor tem acesso conforme as regras do sistema
- [ ] Administrador gerencia usuários e solicitações
- [ ] Tentativas sem permissão retornam resposta explícita
- [ ] A regra de proteção do administrador raiz é preservada

**Labels**
- `security`  
- `rbac`  
- `backend`  
- `priority-high`

---

## Milestone 3 - Consulta de medicamentos e disponibilidade

### Issue 5 - Feature: Implementar consulta pública de medicamentos e disponibilidade por UBS

**Tipo:** feature  
**Prioridade:** Alta

**Descrição**  
O sistema deve permitir a busca e consulta de medicamentos, incluindo visualização da disponibilidade por unidade de saúde.

**Objetivo**
- Consultar medicamentos disponíveis
- Pesquisar por nome ou código
- Apresentar disponibilidade em cada UBS

**Requisitos cobertos**
- RF01 — permitir consulta de medicamentos
- RF02 — permitir busca por nome do medicamento
- RF03 — exibir disponibilidade por UBS
- RF10 — listar UBS cadastradas com disponibilidade
- UC01 — Consultar disponibilidade de medicamentos

**Critérios de aceite**
- [ ] Usuário consegue buscar medicamento por nome
- [ ] Usuário consegue consultar disponibilidade por UBS
- [ ] O sistema exibe quantidade e unidade
- [ ] O sistema retorna mensagem clara quando não houver dado
- [ ] O resultado é paginado e consistente

**Labels**
- `feature`  
- `backend`  
- `frontend`  
- `consulta`  
- `priority-high`

---

### Issue 6 - Feature: Implementar listagem de unidades e filtros por estabelecimento

**Tipo:** feature  
**Prioridade:** Média

**Descrição**  
O usuário deve conseguir listar e filtrar unidades de saúde para consultar a disponibilidade dos medicamentos em diferentes locais.

**Objetivo**
- Exibir estabelecimentos cadastrados
- Permitir filtros por local e medicamento
- Melhorar navegação e consulta

**Critérios de aceite**
- [ ] API retorna listagem de estabelecimentos
- [ ] Frontend consome essa listagem corretamente
- [ ] Usuário pode filtrar por unidade de saúde
- [ ] A busca responde corretamente para diferentes combinações

**Labels**
- `feature`  
- `consulta`  
- `frontend`  
- `priority-medium`

---

## Milestone 4 - Mapa, geolocalização e unidade mais próxima

### Issue 7 - Feature: Implementar mapa interativo com UBS e informações detalhadas

**Tipo:** feature  
**Prioridade:** Alta

**Descrição**  
O sistema deve disponibilizar um mapa interativo para localizar UBS e unidades participantes, além de informações detalhadas de endereço, horário e funcionamento.

**Objetivo**
- Exibir UBS em mapa
- Mostrar informações importantes da unidade
- Melhorar a identificação das opções disponíveis

**Requisitos cobertos**
- RF05 — exibir Farmácia Popular mais próxima
- RF10 — listar UBS cadastradas
- RF11 — mapa interativo
- RF13 — exibir horários de funcionamento
- UC02 — visualizar unidade mais próxima
- UC03 — visualizar informações da unidade

**Critérios de aceite**
- [ ] O mapa exibe as UBS cadastradas
- [ ] Cada unidade possui nome, endereço e horário
- [ ] O usuário consegue selecionar uma unidade no mapa
- [ ] O sistema mostra a disponibilidade do medicamento
- [ ] A interface funciona em desktop, tablet e mobile

**Labels**
- `feature`  
- `mapa`  
- `frontend`  
- `priority-high`

---

### Issue 8 - Feature: Implementar localização do usuário e cálculo da UBS mais próxima

**Tipo:** feature  
**Prioridade:** Alta

**Descrição**  
Como usuário comum, desejo encontrar a unidade mais próxima que tenha o medicamento disponível, para reduzir deslocamentos desnecessários.

**Objetivo**
- Capturar a localização do usuário
- Calcular distância até as UBS disponíveis
- Destacar a unidade mais próxima

**Requisitos cobertos**
- RF04 — informar localização por geolocalização ou endereço
- RF05 — exibir unidade mais próxima
- RF09 — calcular distância
- UC02 — Visualizar unidade mais próxima

**Critérios de aceite**
- [ ] O sistema aceita geolocalização ou endereço
- [ ] O cálculo de distância está correto
- [ ] A unidade mais próxima é identificada para o usuário
- [ ] O sistema exibe opções válidas mesmo quando há múltiplas UBS
- [ ] A mensagem de ausência de medicamento é clara

**Labels**
- `feature`  
- `geolocalizacao`  
- `mapa`  
- `priority-high`

---

### Issue 9 - Feature: Exibir UBS sem farmacêutico e sinalizar unidades com orientação farmacêutica

**Tipo:** feature  
**Prioridade:** Média

**Descrição**  
O sistema deve informar ao usuário se a unidade mais próxima possui farmacêutico, para orientar a escolha da UBS e diferenciar unidades com e sem atendimento farmacêutico.

**Objetivo**
- Indicar presença ou ausência de farmacêutico
- Diferenciar unidades visualmente
- Apoiar o usuário na escolha da unidade

**Requisitos cobertos**
- RF14 — mostrar UBS em que não tem farmacêuticos
- História do usuário comum
- Informação da unidade

**Critérios de aceite**
- [ ] O sistema identifica se a unidade possui farmacêutico
- [ ] A informação é exibida para o usuário
- [ ] O mapa difere visualmente unidades com e sem farmacêutico
- [ ] A regra também se aplica em listagens e seleção da unidade

**Labels**
- `feature`  
- `mapa`  
- `indicadores`  
- `priority-medium`

---

## Milestone 5 - Administração e atualização de dados

### Issue 10 - Feature: Implementar upload de relatórios XLSX e atualização automática do estoque

**Tipo:** feature  
**Prioridade:** Alta

**Descrição**  
Como responsável pelo estoque, desejo enviar relatórios em XLSX para manter o sistema atualizado com as informações reais de medicamentos e unidades de saúde.

**Objetivo**
- Aceitar upload de arquivos XLSX
- Validar o relatório recebido
- Atualizar estoque de forma automática e segura

**Requisitos cobertos**
- RF12 — atualizar automaticamente as informações de estoque
- Atualização de dados em lote
- História do usuário de responsável pelo estoque

**Critérios de aceite**
- [ ] O sistema aceita apenas arquivos XLSX
- [ ] O arquivo é validado antes do processamento
- [ ] O sistema exibe prévia ou confirmação da atualização
- [ ] O estoque é atualizado sem duplicidade
- [ ] O sistema informa sucesso ou erro corretamente

**Labels**
- `feature`  
- `upload`  
- `etl`  
- `priority-high`

---

### Issue 11 - Feature: Permitir atualização de horários e dados cadastrais da UBS

**Tipo:** feature  
**Prioridade:** Média

**Descrição**  
Como prescritor ou administrador, desejo atualizar as informações de funcionamento e cadastro da unidade para manter os dados úteis e confiáveis para os usuários.

**Objetivo**
- Atualizar endereço, horário e dados básicos da UBS
- Garantir segurança do processo
- Manter registro das alterações

**Critérios de aceite**
- [ ] Usuários autorizados atualizam dados da UBS
- [ ] O sistema valida as informações antes de salvar
- [ ] Registro da alteração é mantido
- [ ] Usuários comuns não têm acesso a essa funcionalidade

**Labels**
- `feature`  
- `admin`  
- `autorizacao`  
- `priority-medium`

---

### Issue 12 - Feature: Criar dashboard administrativo para avaliação de uso do sistema

**Tipo:** feature  
**Prioridade:** Média

**Descrição**  
Como gestor da UBS, desejo acompanhar o uso do sistema, avaliar sua efetividade e reunir indicadores úteis para operação e gestão.

**Objetivo**
- Exibir indicadores de uso
- Filtrar dados por período
- Dar visibilidade ao gestor da operação

**Requisitos cobertos**
- História do gestor da UBS
- Acompanhamento do uso do sistema
- Indicadores operacionais

**Critérios de aceite**
- [ ] Dashboard está disponível para administradores
- [ ] Sistema exibe indicadores de uso
- [ ] O gestor consegue filtrar por período
- [ ] Informações refletem dados reais de registro
- [ ] Layout é acessível e funcional

**Labels**
- `feature`  
- `dashboard`  
- `analytics`  
- `priority-medium`

---

## Milestone 6 - Qualidade, performance e requisitos não funcionais

### Issue 13 - Fix: Validar requisitos não funcionais de responsividade, disponibilidade e segurança

**Tipo:** fix  
**Prioridade:** Média

**Descrição**  
O sistema precisa atender critérios de qualidade como responsividade, tempo de resposta, compatibilidade com navegadores e controle de acesso. Esta issue tem como objetivo verificar e corrigir falhas na experiência e segurança do produto.

**Objetivo**
- Garantir tempo adequado de resposta
- Melhorar a experiência em desktop, tablet e mobile
- Preservar segurança e disponibilidade

**Requisitos cobertos**
- RNF01 — interface simples, intuitiva e responsiva
- RNF02 — tempo de resposta inferior a 3 segundos
- RNF04 — compatibilidade com navegadores modernos
- RNF06 — disponibilidade 24/7
- RNF07 — tempo de resposta inferior a 5 segundos
- RNF08 — interface responsiva
- RNF03 — controle de acesso

**Critérios de aceite**
- [ ] O sistema apresenta interface responsiva
- [ ] As consultas atendem aos tempos esperados
- [ ] O sistema funciona em navegadores modernos
- [ ] O acesso administrativo está protegido
- [ ] A aplicação mantém estabilidade básica em uso cotidiano

**Labels**
- `fix`  
- `quality`  
- `performance`  
- `security`  
- `priority-medium`

---

## Resumo da priorização

### Fase 1 - Core do produto
- Issue 1
- Issue 2
- Issue 3
- Issue 5
- Issue 7
- Issue 8
- Issue 10

### Fase 2 - Gestão e experiência
- Issue 4
- Issue 6
- Issue 9
- Issue 11
- Issue 12

### Fase 3 - Qualidade e estabilização
- Issue 13

---

## Conclusão

As issues acima foram organizadas de acordo com o documento de requisitos e refletem:
- objetivos de negócio
- classes de usuários
- casos de uso
- requisitos funcionais
- requisitos não funcionais
- prioridades de execução do projeto

A migração do backend para Django aparece tanto como issue de feature quanto de fix, conforme solicitado, e os demais itens foram estruturados para seguir a lógica do documento oficial do projeto.
