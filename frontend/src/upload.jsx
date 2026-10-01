import { useState, useRef } from "react"
import { apiService } from "./services/api";

const UploadFile = ({ onSuccess }) => {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const fileInputRef = useRef(null)

  const onFileChange = (e) => {
    setFile(e.target.files[0])
  }

  const handleDownloadTemplate = () => {
    const csvContent = [
      [
        "nome_estabelecimento",
        "gestor",
        "telefone",
        "email",
        "endereco",
        "horario",
        "catmat",
        "medicamento",
        "quantidade"
      ],
      [
        "UBS Centro",
        "Ana Souza",
        "(67) 99999-0000",
        "ubs.centro@teste.com",
        "Rua A, 10",
        "08:00-17:00",
        "BR123456",
        "Paracetamol",
        "12"
      ],
      [
        "UBS Centro",
        "Ana Souza",
        "(67) 99999-0000",
        "ubs.centro@teste.com",
        "Rua A, 10",
        "08:00-17:00",
        "BR654321",
        "Ibuprofeno",
        "5"
      ]
    ]
      .map((row) => row.map((value) => `"${String(value).replace(/"/g, '""')}"`).join(","))
      .join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "modelo_upload_achei.csv";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Por favor, selecione um arquivo primeiro!");

    setLoading(true);
    try {
      const response = await apiService.uploadFile(file);
      alert(response.message || "Arquivo enviado com sucesso!");

      setFile(null);
      if (fileInputRef.current) fileInputRef.current.value = "";

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
        Selecione uma planilha em Excel ou CSV. O sistema aceita tanto o formato antigo quanto o formato com colunas nomeadas: nome_estabelecimento, catmat, medicamento, quantidade e campos extras do estabelecimento.
      </p>

      <div className="alert alert-light border mb-3 small text-muted">
        Cabeçalhos suportados: nome_estabelecimento, gestor, telefone, email, endereco, horario, catmat, medicamento, quantidade.
      </div>

      <div className="d-flex justify-content-end mb-3">
        <button type="button" className="btn btn-outline-primary btn-sm" onClick={handleDownloadTemplate}>
          Baixar modelo CSV
        </button>
      </div>

      <form onSubmit={onSubmit} className="d-flex align-items-center gap-3 flex-wrap">
        <div className="flex-grow-1">
          <input
            type="file"
            className="form-control"
            id="file"
            onChange={onFileChange}
            ref={fileInputRef}
            accept=".xls,.xlsx,.csv"
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
