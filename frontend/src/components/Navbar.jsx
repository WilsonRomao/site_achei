import React from 'react';

const Navbar = ({ user, onLogout, onRestrictedArea }) => {

  return (
    <header className="site-header">
      <div className="site-container site-header-inner">
        <div className="brand-lockup">
          <a className="brand-name" href="#inicio">ACHEI!</a>
          <span>Rede básica de saúde</span>
        </div>

        {!user ? (
          <button className="header-action" onClick={onRestrictedArea}>
            Área restrita
          </button>
        ) : (
          <div className="user-menu">
            <span className="user-label">{user.email}</span>
            <button className="header-action header-action-light" onClick={onLogout}>
              Sair
            </button>
          </div>
        )}
      </div>
    </header>
  );
};

export default Navbar;
