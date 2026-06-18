import { useState, useRef } from "react"
import { apiService } from "./services/api";

const UploadFile = ({ onSuccess }) => {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const fileInputRef = useRef(null)

  const onFileChange = (e) => {
    setFile(e.target.files[0])
  }

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Por favor, selecione um arquivo primeiro!");

    setLoading(true);
    try {
      const response = await apiService.uploadFile(file);
      alert(response.message || "Arquivo enviado com sucesso!");
      
      // Limpa os estados
      setFile(null);
      if (fileInputRef.current) fileInputRef.current.value = "";
      
      // Chama o hook de sucesso para recarregar os dados na tabela
      if (onSuccess) onSuccess(); 
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card border-0 shadow-sm rounded-4 p-4 mb-4" style={{ backgroundColor: "#eef8fa" }}>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h5 className="mb-0 fw-bold" style={{ color: "var(--achei-blue)" }}>
          <i className="bi bi-cloud-arrow-up me-2"></i>
          Atualização de Estoque
        </h5>
        <span className="badge bg-warning text-dark">Painel do Administrador</span>
      </div>
      
      <p className="text-muted small mb-3">
        Selecione a planilha Excel mais recente (.xls ou .xlsx) contendo os dados dos estoques de todas as unidades.
      </p>

      <form onSubmit={onSubmit} className="d-flex align-items-center gap-3">
        <div className="flex-grow-1">
          <input 
            type="file" 
            className="form-control" 
            id="file" 
            onChange={onFileChange} 
            ref={fileInputRef}
            accept=".xls,.xlsx"
          />
        </div>
        <button 
          type="submit" 
          className="btn text-white px-4 fw-bold" 
          style={{ backgroundColor: "var(--achei-teal)" }}
          disabled={loading || !file}
        >
          {loading ? (
            <><span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Enviando...</>
          ) : (
            "Enviar Planilha"
          )}
        </button>
      </form>
    </div>
  )
}

export default UploadFile
