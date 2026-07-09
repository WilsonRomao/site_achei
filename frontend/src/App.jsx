import { useState, useEffect, useCallback } from 'react'
import MedicamentoList from './MedicamentoList' 
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
  
  const [medicamentos, setMedicamentos] = useState([])
  const [listaEstabelecimentos, setListaEstabelecimentos] = useState([])
  const [loading, setLoading] = useState(false)
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)

  const [filtros, setFiltros] = useState({
    q: '',
    catmat: '',
    estabelecimento: ''
  })

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
      }
    }
  }, []);

  useEffect(() => {
    if (!user) return;
    const carregarEstabelecimentos = async () => {
      try {
        const dados = await apiService.getEstabelecimentos();
        setListaEstabelecimentos(dados);
      } catch (error) {
        console.error(error);
      }
    };
    carregarEstabelecimentos();
  }, [user]);

  const fetchMedicamentos = useCallback(async () => {
    if (!user) return;
    setLoading(true)
    try {
      const data = await apiService.getMedicamentos({ page, ...filtros });
      setMedicamentos(data.items || []) 
      setTotalPages(data.pages || 1)
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }, [page, filtros, user]);

  useEffect(() => {
    fetchMedicamentos()
  }, [fetchMedicamentos])

  const handleFilterChange = (novoFiltro) => {
    setFiltros(prev => ({ ...prev, ...novoFiltro }))
    setPage(1)
  }

  const handleUploadSuccess = () => {
    fetchMedicamentos();
  }

  const handleLogout = () => {
    apiService.logout();
    setUser(null);
  }

  if (!user) {
    return <Auth onLogin={setUser} />;
  }

  return (
    <div className="app-wrapper bg-light min-vh-100">
      <Navbar user={user} onLogout={handleLogout} />
      <Hero />
      
      <main className="container pb-5">
        <Mapa />
        
        {user.perfis.includes("administrador") && (
          <div className="mt-4">
            <UploadFile onSuccess={handleUploadSuccess} />
            <div className="mt-4">
              <AdminPanel />
            </div>
          </div>
        )}
        
        <MedicamentoList 
          medicamentos={medicamentos} 
          listaEstabelecimentos={listaEstabelecimentos}
          filtros={filtros}
          onFilterChange={handleFilterChange}
          page={page}
          setPage={setPage}
          totalPages={totalPages}
          loading={loading}
        />
      </main>
    </div>
  )
}

export default App