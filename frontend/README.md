# ACHEI - Frontend (Client)

A interface com a qual o usuário interage. Desenvolvida em **React** (utilizando **Vite** para empacotamento ultrarrápido) e inteiramente estilizada usando os padrões de grade e utilitários modernos do **Bootstrap 5**.

## 🎨 Design e UI/UX

O visual foi projetado para ser leve, rápido e idêntico a um protótipo focado em saúde pública:
- Uso pesado de **Cores Frias e Profissionais**: Verde-água (`#38b2ac`), Azul Marinho (`#1a365d`) e Cinza (`#6c757d`).
- O **Hero Banner** da página inicial foi inteiramente escrito usando Flexbox CSS e Ícones SVG, eliminando a necessidade de carregar imagens pesadas, garantindo nitidez absoluta em telas de celular ou monitores 4K.
- **Tipografia**: Importação automática da família "Outfit" via Google Fonts para um tom limpo e amigável.
- **Micro-interações**: Uso intensivo de Modais (Janelas Pop-up), Dropdowns e Spinners de carregamento assíncrono para que o usuário não ache que o sistema "travou" durante buscas.

## 🧱 Arquitetura de Componentes

- `App.jsx`: Orquestrador. Guarda o estado de acesso da pessoa (Se está logada e quais são os seus perfis). Bloqueia áreas restritas visualmente para não poluírem a tela de quem é perfil "Padrão".
- `/components/Navbar.jsx`: Barra de navegação com menu interativo onde o usuário lê seus múltiplos cargos e lança solicitações formais para ser promovido (ex: Médico Prescritor).
- `/components/AdminPanel.jsx`: O coração da moderação. Exibido apenas para Administradores. Possui um sistema de abas para Aprovar Requisições ou Cadastrar novos colegas de equipe sob demanda.
- `MedicamentoList.jsx`: Exibe a tabela "Zebrada" (Clean Table) de estoques conectada diretamente ao Banco PostgreSQL via paginação para poupar memória.
- `services/api.js`: Abstração de todo o `fetch()` assíncrono. Cuida da injeção autônoma do `Bearer Token` JWT no cabeçalho das requisições seguras da API Flask.

## 🔧 Scripts Úteis

Para desenvolver e testar sem precisar reiniciar os containers do Docker inteiros, dentro da pasta do frontend, você pode usar:

```bash
# Instalar todos os pacotes caso adicione algo novo
npm install

# Rodar o servidor Node do Vite (Live-Reload agressivo)
npm run dev
```
