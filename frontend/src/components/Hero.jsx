import React from 'react';

const Hero = () => {
  return (
    <div className="hero-banner">
      <div className="container">
        <div className="hero-content">
          <div className="hero-icon">
            {/* Lupa com uma cruz (simulado com ícones sobrepostos ou simples zoom-in) */}
            <i className="bi bi-search" style={{ position: 'relative' }}>
              <i className="bi bi-plus" style={{ position: 'absolute', top: '15px', left: '20px', fontSize: '3rem', color: 'white' }}></i>
            </i>
          </div>
          <h1 className="hero-title">Achei!</h1>
        </div>
        <p className="hero-subtitle">Consulta de Medicamentos - UBS</p>
      </div>
    </div>
  );
};

export default Hero;
