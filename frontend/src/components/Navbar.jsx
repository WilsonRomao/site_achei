import React, { useState } from 'react';
import { apiService } from '../services/api';

const Navbar = ({ user, onLogout }) => {
  const [perfilSelecionado, setPerfilSelecionado] = useState('prescritor');
  const [loading, setLoading] = useState(false);

  const handleSolicitar = async () => {
    setLoading(true);
    try {
      const res = await apiService.solicitarPerfil(perfilSelecionado);
      alert(res.message);
      // Oculta o modal (solução rápida via JS do Bootstrap)
      const modal = document.getElementById('solicitarPerfilModal');
      const bootstrapModal = window.bootstrap.Modal.getInstance(modal);
      bootstrapModal.hide();
    } catch (e) {
      alert(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <nav className="navbar navbar-expand-lg" style={{ backgroundColor: 'var(--achei-teal)' }}>
        <div className="container">
          <a className="navbar-brand text-white fw-bold" href="#">
            <i className="bi bi-search me-2"></i>
            Achei!
          </a>
          
          <button className="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span className="navbar-toggler-icon"></span>
          </button>

          <div className="collapse navbar-collapse justify-content-end" id="navbarNav">
            <ul className="navbar-nav align-items-center">
              <li className="nav-item">
                <a className="nav-link text-white" href="#">Consulta</a>
              </li>
              <li className="nav-item dropdown">
                <a className="nav-link dropdown-toggle text-white" href="#" role="button" data-bs-toggle="dropdown">
                  Prescritores
                </a>
                <ul className="dropdown-menu dropdown-menu-end">
                  <li><a className="dropdown-item" href="#">Área Restrita</a></li>
                </ul>
              </li>
              <li className="nav-item ms-lg-3">
                <i className="bi bi-search text-white fw-bold"></i>
              </li>
              
              {user && (
                <li className="nav-item dropdown ms-lg-4 mt-2 mt-lg-0">
                  <button className="btn btn-sm btn-outline-light rounded-pill px-3 dropdown-toggle" data-bs-toggle="dropdown">
                    <i className="bi bi-person-circle me-1"></i>
                    {user.email.split('@')[0]}
                  </button>
                  <ul className="dropdown-menu dropdown-menu-end shadow border-0 p-3" style={{ minWidth: "250px" }}>
                    <li className="mb-2">
                      <span className="text-muted small fw-bold text-uppercase">Meus Perfis</span>
                      <div className="d-flex flex-wrap gap-1 mt-1">
                        {user.perfis.map(p => (
                          <span key={p} className="badge bg-info text-dark">{p}</span>
                        ))}
                      </div>
                    </li>
                    <li><hr className="dropdown-divider" /></li>
                    <li>
                      <button className="dropdown-item text-primary" data-bs-toggle="modal" data-bs-target="#solicitarPerfilModal">
                        <i className="bi bi-person-plus me-2"></i> Solicitar Novo Perfil
                      </button>
                    </li>
                    <li>
                      <button className="dropdown-item text-danger" onClick={onLogout}>
                        <i className="bi bi-box-arrow-right me-2"></i> Sair do Sistema
                      </button>
                    </li>
                  </ul>
                </li>
              )}
            </ul>
          </div>
        </div>
      </nav>

      {/* Modal de Solicitação */}
      <div className="modal fade" id="solicitarPerfilModal" tabIndex="-1" aria-hidden="true">
        <div className="modal-dialog modal-dialog-centered">
          <div className="modal-content border-0 shadow rounded-4">
            <div className="modal-header border-bottom-0">
              <h5 className="modal-title fw-bold text-dark">
                <i className="bi bi-shield-lock text-info me-2"></i>
                Solicitar Acesso
              </h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div className="modal-body py-2">
              <p className="text-muted small">Selecione o nível de permissão que você deseja solicitar ao Administrador do sistema:</p>
              <select 
                className="form-select form-select-lg bg-light"
                value={perfilSelecionado}
                onChange={(e) => setPerfilSelecionado(e.target.value)}
              >
                <option value="prescritor">Prescritor</option>
                <option value="administrador">Administrador</option>
              </select>
            </div>
            <div className="modal-footer border-top-0 pt-0">
              <button type="button" className="btn btn-light rounded-pill px-4" data-bs-dismiss="modal">Cancelar</button>
              <button 
                type="button" 
                className="btn text-white rounded-pill px-4 fw-bold" 
                style={{ backgroundColor: 'var(--achei-teal)' }}
                onClick={handleSolicitar}
                disabled={loading}
              >
                {loading ? "Enviando..." : "Enviar Solicitação"}
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Navbar;
