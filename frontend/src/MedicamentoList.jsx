import React from "react";

const MedicamentoList = ({ 
  medicamentos, 
  listaEstabelecimentos, 
  filtros, 
  onFilterChange, 
  page, 
  setPage, 
  totalPages, 
  loading 
}) => {
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    onFilterChange({ [name]: value });
  };

  return (
    <div className="mt-5">
      <h4 className="achei-title mb-4">
        Pesquisa de medicamentos disponíveis nas unidades básicas de saúde (UBS)
      </h4>

      <div className="row g-3 mb-4">
        <div className="col-12 col-md-8">
          <div className="input-group input-group-lg">
            <input 
              name="q" 
              className="form-control custom-search-input border-end-0" 
              placeholder="O que precisa achar hoje?" 
              value={filtros.q} 
              onChange={handleChange} 
            />
            <span className="input-group-text custom-search-btn bg-white">
              <i className="bi bi-search"></i>
            </span>
          </div>
        </div>
        <div className="col-12 col-md-4">
          <input 
            name="estabelecimento" 
            list="lista-estabelecimentos" 
            className="form-control form-control-lg custom-search-input"
            placeholder="Filtrar por Estabelecimento..." 
            value={filtros.estabelecimento} 
            onChange={handleChange} 
          />
          <datalist id="lista-estabelecimentos">
            {listaEstabelecimentos.map((est, index) => (
              <option key={index} value={est} />
            ))}
          </datalist>
        </div>
      </div>

      <div className="card border-0 shadow-sm rounded-4 overflow-hidden">
        {loading ? (
          <div className="text-center p-5 text-muted">
            <div className="spinner-border text-info" role="status">
              <span className="visually-hidden">Carregando...</span>
            </div>
            <p className="mt-2">Buscando estoques...</p>
          </div>
        ) : (
          <>
            <table className="table table-striped table-hover mb-0 align-middle">
              <thead className="table-light text-muted">
                <tr>
                  <th className="ps-4 py-3 fw-normal">Medicamento</th>
                  <th className="py-3 fw-normal">Estabelecimento</th>
                  <th className="py-3 fw-normal text-center">Quantidade</th>
                </tr>
              </thead>
              <tbody>
                {medicamentos.length > 0 ? medicamentos.map((item, index) => (
                  <tr key={`${item.catmat}-${item.estabelecimentoSaude}-${index}`}>
                    <td className="ps-4 py-3 text-dark">{item.medicamento}</td>
                    <td className="py-3 text-secondary">{item.estabelecimentoSaude}</td>
                    <td className="py-3 text-center">
                      <span className={`badge rounded-pill ${item.quantidade > 0 ? 'bg-success' : 'bg-danger'}`}>
                        {item.quantidade}
                      </span>
                    </td>
                  </tr>
                )) : (
                  <tr>
                    <td colSpan="3" className="text-center py-5 text-muted">Nenhum medicamento encontrado para essa busca.</td>
                  </tr>
                )}
              </tbody>
            </table>

            <div className="card-footer bg-white border-top-0 d-flex justify-content-between align-items-center py-3 px-4">
              <button 
                className="btn btn-outline-secondary rounded-pill px-4" 
                disabled={page === 1} 
                onClick={() => setPage(p => p - 1)}>
                Anterior
              </button>
              <span className="text-muted small">Página {page} de {totalPages}</span>
              <button 
                className="btn btn-outline-secondary rounded-pill px-4" 
                disabled={page === totalPages} 
                onClick={() => setPage(p => p + 1)}>
                Próximo
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default MedicamentoList;