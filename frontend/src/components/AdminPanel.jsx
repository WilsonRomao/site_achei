import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const AdminPanel = () => {
  const [activeTab, setActiveTab] = useState('usuarios');
  const [usuarios, setUsuarios] = useState([]);
  const [solicitacoes, setSolicitacoes] = useState([]);
  const [loading, setLoading] = useState(false);

  // Form states for new user
  const [novoEmail, setNovoEmail] = useState('');
  const [novaSenha, setNovaSenha] = useState('');
  const [novoPerfis, setNovoPerfis] = useState(['padrão']);
  const [criandoUser, setCriandoUser] = useState(false);

  useEffect(() => {
    carregarDados();
  }, [activeTab]);

  const carregarDados = async () => {
    setLoading(true);
    try {
      if (activeTab === 'usuarios') {
        const data = await apiService.getUsuarios();
        setUsuarios(data);
      } else {
        const data = await apiService.getSolicitacoes();
        setSolicitacoes(data);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const togglePerfil = async (usuario, perfil) => {
    try {
      const temPerfil = usuario.perfis.includes(perfil);
      let novosPerfis = [...usuario.perfis];
      
      if (temPerfil) {
        novosPerfis = novosPerfis.filter(p => p !== perfil);
      } else {
        novosPerfis.push(perfil);
      }

      await apiService.setUsuarioPerfis(usuario.id, novosPerfis);
      carregarDados();
    } catch (error) {
      alert(error.message);
    }
  };

  const processarSolicitacao = async (id, acao) => {
    try {
      await apiService.processarSolicitacao(id, acao);
      carregarDados();
      alert(`Solicitação ${acao === 'aprovar' ? 'Aprovada' : 'Recusada'}!`);
    } catch (error) {
      alert(error.message);
    }
  };

  const handleCriarUsuario = async (e) => {
    e.preventDefault();
    setCriandoUser(true);
    try {
      await apiService.criarUsuario(novoEmail, novaSenha, novoPerfis);
      alert("Usuário criado com sucesso!");
      setNovoEmail('');
      setNovaSenha('');
      setNovoPerfis(['padrão']);
      carregarDados();
      // Fechar modal via JS do Bootstrap
      const modal = document.getElementById('criarUsuarioModal');
      const bootstrapModal = window.bootstrap.Modal.getInstance(modal);
      if (bootstrapModal) bootstrapModal.hide();
    } catch (error) {
      alert(error.message);
    } finally {
      setCriandoUser(false);
    }
  };

  const toggleNovoPerfil = (perfil) => {
    if (novoPerfis.includes(perfil)) {
      setNovoPerfis(novoPerfis.filter(p => p !== perfil));
    } else {
      setNovoPerfis([...novoPerfis, perfil]);
    }
  };

  return (
    <>
      <div className="card shadow-sm border-0 rounded-4 mb-4">
        <div className="card-header bg-white border-bottom-0 pt-4 pb-0 d-flex justify-content-between align-items-end">
          <ul className="nav nav-tabs border-bottom-0">
            <li className="nav-item">
              <button 
                className={`nav-link fw-bold border-0 ${activeTab === 'usuarios' ? 'text-dark border-bottom border-3 border-info' : 'text-muted'}`}
                onClick={() => setActiveTab('usuarios')}
              >
                <i className="bi bi-people me-2"></i>
                Gerenciar Usuários
              </button>
            </li>
            <li className="nav-item">
              <button 
                className={`nav-link fw-bold border-0 ${activeTab === 'solicitacoes' ? 'text-dark border-bottom border-3 border-info' : 'text-muted'}`}
                onClick={() => setActiveTab('solicitacoes')}
              >
                <i className="bi bi-envelope-paper me-2"></i>
                Solicitações de Perfil
              </button>
            </li>
          </ul>
          {activeTab === 'usuarios' && (
            <button className="btn btn-sm btn-success mb-2" data-bs-toggle="modal" data-bs-target="#criarUsuarioModal">
              <i className="bi bi-person-plus-fill me-1"></i> Criar Usuário
            </button>
          )}
        </div>
        
        <div className="card-body p-4 bg-light rounded-bottom-4">
          {loading ? (
            <div className="text-center py-4"><span className="spinner-border text-info"></span></div>
          ) : (
            activeTab === 'usuarios' ? (
              <div className="table-responsive bg-white rounded-3 p-3">
                <table className="table table-hover align-middle mb-0">
                  <thead>
                    <tr>
                      <th>Email do Usuário</th>
                      <th className="text-center">Padrão</th>
                      <th className="text-center">Prescritor</th>
                      <th className="text-center">Administrador</th>
                    </tr>
                  </thead>
                  <tbody>
                    {usuarios.map(u => (
                      <tr key={u.id}>
                        <td className="fw-bold text-secondary">{u.email}</td>
                        <td className="text-center">
                          <input type="checkbox" className="form-check-input" 
                            checked={u.perfis.includes('padrão')} 
                            onChange={() => togglePerfil(u, 'padrão')} 
                          />
                        </td>
                        <td className="text-center">
                          <input type="checkbox" className="form-check-input" 
                            checked={u.perfis.includes('prescritor')} 
                            onChange={() => togglePerfil(u, 'prescritor')} 
                          />
                        </td>
                        <td className="text-center">
                          <input type="checkbox" className="form-check-input" 
                            checked={u.perfis.includes('administrador')} 
                            onChange={() => togglePerfil(u, 'administrador')} 
                            disabled={u.email === 'admin@achei.com'}
                          />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="table-responsive bg-white rounded-3 p-3">
                <table className="table table-hover align-middle mb-0">
                  <thead>
                    <tr>
                      <th>Data</th>
                      <th>Usuário</th>
                      <th>Perfil Solicitado</th>
                      <th>Status</th>
                      <th className="text-end">Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {solicitacoes.length === 0 ? (
                      <tr><td colSpan="5" className="text-center py-3 text-muted">Nenhuma solicitação encontrada.</td></tr>
                    ) : solicitacoes.map(s => (
                      <tr key={s.id}>
                        <td>{s.data_solicitacao}</td>
                        <td className="fw-bold">{s.email_usuario}</td>
                        <td><span className="badge bg-secondary">{s.perfil_solicitado}</span></td>
                        <td>
                          <span className={`badge ${s.status === 'pendente' ? 'bg-warning text-dark' : (s.status === 'aprovado' ? 'bg-success' : 'bg-danger')}`}>
                            {s.status}
                          </span>
                        </td>
                        <td className="text-end">
                          {s.status === 'pendente' && (
                            <>
                              <button className="btn btn-sm btn-success me-2" onClick={() => processarSolicitacao(s.id, 'aprovar')}>
                                <i className="bi bi-check-circle"></i> Aprovar
                              </button>
                              <button className="btn btn-sm btn-danger" onClick={() => processarSolicitacao(s.id, 'recusar')}>
                                <i className="bi bi-x-circle"></i> Recusar
                              </button>
                            </>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )
          )}
        </div>
      </div>

      {/* Modal Criar Usuario */}
      <div className="modal fade" id="criarUsuarioModal" tabIndex="-1" aria-hidden="true">
        <div className="modal-dialog modal-dialog-centered">
          <div className="modal-content border-0 shadow rounded-4">
            <div className="modal-header border-bottom-0">
              <h5 className="modal-title fw-bold text-dark">Criar Novo Usuário</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form onSubmit={handleCriarUsuario}>
              <div className="modal-body py-2">
                <div className="mb-3">
                  <label className="form-label text-muted small fw-bold">E-mail</label>
                  <input type="email" required className="form-control" value={novoEmail} onChange={(e) => setNovoEmail(e.target.value)} />
                </div>
                <div className="mb-3">
                  <label className="form-label text-muted small fw-bold">Senha</label>
                  <input type="password" required className="form-control" value={novaSenha} onChange={(e) => setNovaSenha(e.target.value)} />
                </div>
                <div className="mb-3">
                  <label className="form-label text-muted small fw-bold">Perfis Iniciais</label>
                  <div className="d-flex gap-3 mt-1">
                    <div className="form-check">
                      <input className="form-check-input" type="checkbox" checked={novoPerfis.includes('padrão')} onChange={() => toggleNovoPerfil('padrão')} />
                      <label className="form-check-label">Padrão</label>
                    </div>
                    <div className="form-check">
                      <input className="form-check-input" type="checkbox" checked={novoPerfis.includes('prescritor')} onChange={() => toggleNovoPerfil('prescritor')} />
                      <label className="form-check-label">Prescritor</label>
                    </div>
                    <div className="form-check">
                      <input className="form-check-input" type="checkbox" checked={novoPerfis.includes('administrador')} onChange={() => toggleNovoPerfil('administrador')} />
                      <label className="form-check-label">Admin</label>
                    </div>
                  </div>
                </div>
              </div>
              <div className="modal-footer border-top-0 pt-0">
                <button type="button" className="btn btn-light rounded-pill px-4" data-bs-dismiss="modal">Cancelar</button>
                <button type="submit" className="btn btn-success rounded-pill px-4" disabled={criandoUser}>
                  {criandoUser ? "Criando..." : "Salvar Usuário"}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </>
  );
};

export default AdminPanel;
