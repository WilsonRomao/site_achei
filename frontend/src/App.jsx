import { useState, useEffect, useCallback } from 'react'
import UploadFile from './upload'
import Auth from './Auth'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import AdminPanel from './components/AdminPanel'
import { apiService } from './services/api'
import './App.css'
import Mapa from './Mapa';

function App() {
  const [user, setUser] = useState(null)
  const [showAuth, setShowAuth] = useState(false)
  const [restrictedArea, setRestrictedArea] = useState(false)
  const [unidadeSelecionada, setUnidadeSelecionada] = useState(null)
  const [estoqueUnidade, setEstoqueUnidade] = useState([])
  const [carregandoEstoque, setCarregandoEstoque] = useState(false)
  const [erroEstoque, setErroEstoque] = useState("")

  useEffect(() => {
    const savedUser = localStorage.getItem("usuario");
    if (savedUser) {
      const parsedUser = JSON.parse(savedUser);
      // Proteção contra cache da versão antiga (antes dos múltiplos perfis)
      if (!parsedUser.perfis) {
        localStorage.removeItem("usuario");
        localStorage.removeItem("token");
        window.location.reload();
      } else {
        setUser(parsedUser);
        setRestrictedArea(false);
      }
    }
  }, []);

  const handleLogout = () => {
    apiService.logout();
    setUser(null);
    setShowAuth(false);
    setRestrictedArea(false);
  }

  const handleLogin = (loggedUser) => {
    setUser(loggedUser);
    setShowAuth(false);
    setRestrictedArea(true);
  }

  const handleUnidadeSelecionada = useCallback((unidade) => {
    setUnidadeSelecionada(unidade)
  }, [])

  useEffect(() => {
    if (!unidadeSelecionada) {
      setEstoqueUnidade([])
      return undefined
    }

    let ativo = true
    setCarregandoEstoque(true)
    setErroEstoque("")

    apiService.getEstoquePorEstabelecimento(unidadeSelecionada.nome)
      .then((dados) => {
        if (ativo) setEstoqueUnidade(dados.items || [])
      })
      .catch(() => {
        if (ativo) {
          setEstoqueUnidade([])
          setErroEstoque("Não foi possível carregar os medicamentos desta unidade.")
        }
      })
      .finally(() => {
        if (ativo) setCarregandoEstoque(false)
      })

    return () => {
      ativo = false
    }
  }, [unidadeSelecionada])

  if (showAuth && !restrictedArea) {
    return <Auth onLogin={handleLogin} onBack={() => setShowAuth(false)} />;
  }

  return (
    <div className="app-wrapper">
      <Navbar
        user={restrictedArea ? user : null}
        onLogout={handleLogout}
        onRestrictedArea={() => {
          if (user) {
            setRestrictedArea(true);
          } else {
            setShowAuth(true);
          }
        }}
      />
      <Hero />
      <main className="site-container">
        <div className="breadcrumb-line">Mapa interativo / Unidades de Saúde / Detalhes da unidade</div>

        <div className={`layout-grid ${restrictedArea && user ? "layout-grid-restricted" : "layout-grid-public"}`}>
          <section>
            <article className="reference-card map-card">
              <h3>Localização</h3>
              <Mapa onSelectUnidade={handleUnidadeSelecionada} />
            </article>

            <article className="reference-card selected-unit-card">
              <h3>Unidades de Saúde</h3>
              {unidadeSelecionada ? (
                <div className="unit-details-grid">
                  <div className="info-item"><strong>Unidade</strong><p>{unidadeSelecionada.nome}</p></div>
                  <div className="info-item"><strong>CNES</strong><p>{unidadeSelecionada.cnes || "Não informado"}</p></div>
                  <div className="info-item"><strong>Endereço</strong><p>{unidadeSelecionada.endereco || "Não informado"}</p></div>
                  <div className="info-item"><strong>Telefone</strong><p>{unidadeSelecionada.telefone || "Não informado"}</p></div>
                  <div className="info-item"><strong>Horário de funcionamento</strong><p>{unidadeSelecionada.horario || "Não informado"}</p></div>
                  <div className="info-item"><strong>Farmacêutico</strong><p className={unidadeSelecionada.farmaceutico ? "available-text" : "unavailable-text"}>{unidadeSelecionada.farmaceutico ? "Sim" : "Não"}</p></div>
                  {unidadeSelecionada.horario_farmaceutico && <div className="info-item"><strong>Horário do farmacêutico</strong><p>{unidadeSelecionada.horario_farmaceutico}</p></div>}
                  {unidadeSelecionada.link && <div className="info-item"><strong>Informações oficiais</strong><p><a href={unidadeSelecionada.link} target="_blank" rel="noreferrer">Consultar página da unidade</a></p></div>}
                </div>
              ) : (
                <p className="map-message">Clique em um marcador no mapa para ver os detalhes da unidade.</p>
              )}
              {unidadeSelecionada && (
                <div className="unit-stock">
                  <h4>Medicamentos disponíveis na unidade</h4>
                  {carregandoEstoque && <p className="map-message">Carregando estoque...</p>}
                  {erroEstoque && <p className="map-message map-error">{erroEstoque}</p>}
                  {!carregandoEstoque && !erroEstoque && estoqueUnidade.length === 0 && (
                    <p className="map-message">Nenhum medicamento cadastrado para esta unidade.</p>
                  )}
                  {!carregandoEstoque && !erroEstoque && estoqueUnidade.length > 0 && (
                    <div className="stock-table-wrapper">
                      <table className="stock-table">
                        <thead>
                          <tr>
                            <th>Medicamento</th>
                            <th>Status</th>
                            {restrictedArea && user && <th>Quantidade</th>}
                          </tr>
                        </thead>
                        <tbody>
                          {estoqueUnidade.map((item) => {
                            const disponivel = Number(item.quantidade) > 0
                            return (
                              <tr key={`${item.catmat}-${item.medicamento}`}>
                                <td>{item.medicamento}</td>
                                <td className={disponivel ? "available-text" : "unavailable-text"}>
                                  {disponivel ? "Disponível" : "Indisponível"}
                                </td>
                                {restrictedArea && user && <td>{item.quantidade}</td>}
                              </tr>
                            )
                          })}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              )}
            </article>

            <article className="reference-card">
              <h3>Serviços da rede</h3>
              <ul className="service-list">
                <li>Atendimento médico e de enfermagem</li>
                <li>Dispensação de medicamentos</li>
                <li>Vacinação e acompanhamento de saúde</li>
                <li>Curativos e procedimentos básicos</li>
              </ul>
            </article>
          </section>

          <aside>
            {restrictedArea && user && (
              <section className="reference-card restricted-card">
                <h3>Área restrita</h3>
                <p>Informações do usuário autenticado.</p>
                <dl className="user-details">
                  <dt>E-mail</dt><dd>{user.email}</dd>
                  <dt>Identificador</dt><dd>{user.id}</dd>
                  <dt>Perfis</dt><dd><span className="profile-list">{user.perfis.map((perfil) => <span key={perfil}>{perfil}</span>)}</span></dd>
                </dl>
                {user.perfis.includes("administrador") && <><UploadFile /><AdminPanel /></>}
              </section>
            )}
          </aside>
        </div>
      </main>

      <footer className="site-footer">ACHEI! - Rede básica de saúde<br />Projeto PET-Saúde Digital | UFMS e SESAU</footer>
    </div>
  )
}

export default App