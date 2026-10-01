import React from 'react';

const Hero = () => {
  return (
    <div className="hero-banner">
      <div className="site-container hero-content">
        <div>
          <p className="hero-eyebrow">Informação pública em saúde</p>
          <h1 className="hero-title">ACHEI!</h1>
          <p className="hero-subtitle">Mapa público da rede de saúde</p>
        </div>
        <div className="hero-mark" aria-hidden="true">+</div>
      </div>
    </div>
  );
};

export default Hero;
