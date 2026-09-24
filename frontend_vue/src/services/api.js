const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

// Helper para obter os headers padrões com o Token
const getHeaders = () => {
  const token = localStorage.getItem("token");
  return token ? { "Authorization": `Bearer ${token}` } : {};
};

export const apiService = {
  async register(email, senha) {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, senha })
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.message || "Erro no cadastro");
    }
    return response.json();
  },

  async solicitarPerfil(perfil) {
    const response = await fetch(`${API_BASE_URL}/auth/solicitar`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...getHeaders() },
      body: JSON.stringify({ perfil })
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.message || "Erro ao solicitar");
    }
    return response.json();
  },

  async getUsuarios() {
    const response = await fetch(`${API_BASE_URL}/admin/usuarios`, { headers: getHeaders() });
    if (!response.ok) throw new Error("Erro ao buscar usuários");
    return response.json();
  },

  async criarUsuario(email, senha, perfis) {
    const response = await fetch(`${API_BASE_URL}/admin/usuarios`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...getHeaders() },
      body: JSON.stringify({ email, senha, perfis })
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.message || "Erro ao criar usuário");
    }
    return response.json();
  },

  async setUsuarioPerfis(id, perfis) {
    const response = await fetch(`${API_BASE_URL}/admin/usuarios/${id}/perfis`, {
      method: "PUT",
      headers: { "Content-Type": "application/json", ...getHeaders() },
      body: JSON.stringify({ perfis })
    });
    if (!response.ok) throw new Error("Erro ao atualizar perfis");
    return response.json();
  },

  async getSolicitacoes() {
    const response = await fetch(`${API_BASE_URL}/admin/solicitacoes`, { headers: getHeaders() });
    if (!response.ok) throw new Error("Erro ao buscar solicitações");
    return response.json();
  },

  async processarSolicitacao(id, acao) {
    const response = await fetch(`${API_BASE_URL}/admin/solicitacoes/${id}/${acao}`, {
      method: "POST",
      headers: getHeaders()
    });
    if (!response.ok) throw new Error(`Erro ao ${acao} solicitação`);
    return response.json();
  },


  async login(email, senha) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, senha })
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.message || "Credenciais inválidas");
    }
    const data = await response.json();
    localStorage.setItem("token", data.token);
    localStorage.setItem("usuario", JSON.stringify(data.usuario));
    return data;
  },

  logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
  },

  async getEstabelecimentos() {
    const response = await fetch(`${API_BASE_URL}/estabelecimentos`, {
      headers: getHeaders()
    });
    if (!response.ok) throw new Error("Erro ao buscar estabelecimentos");
    return response.json();
  },

  async getMedicamentos(params) {
    const query = new URLSearchParams(params).toString();
    const response = await fetch(`${API_BASE_URL}/medicamentos?${query}`, {
      headers: getHeaders()
    });
    if (!response.ok) throw new Error("Erro ao carregar medicamentos");
    return response.json();
  },

  async uploadFile(file) {
    const formData = new FormData();
    formData.append("file", file);
    
    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: "POST",
      headers: getHeaders(), // O fetch cuida do Content-Type multipart boundary sozinho
      body: formData,
    });
    
    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.message || "Falha no upload");
    }
    return response.json();
  }
};
