import { useState } from "react";
import { apiService } from "./services/api";

const Auth = ({ onLogin }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [perfil, setPerfil] = useState("padrão");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (isLogin) {
        const data = await apiService.login(email, senha);
        onLogin(data.usuario);
      } else {
        await apiService.register(email, senha);
        alert("Cadastro realizado! O seu usuário Padrão foi criado. Faça o login.");
        setIsLogin(true);
        setSenha("");
      }
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
      <div className="card shadow-sm border-0 p-4 rounded-4" style={{ width: "100%", maxWidth: "400px" }}>
        
        <div className="text-center mb-4">
          <i className="bi bi-shield-lock text-primary" style={{ fontSize: "3rem", color: "var(--achei-teal) !important" }}></i>
          <h3 className="fw-bold text-dark mt-2">{isLogin ? "Acesso Restrito" : "Novo Cadastro"}</h3>
          <p className="text-muted small">
            {isLogin ? "Faça login para consultar o estoque das UBS" : "Cadastre-se para acessar o sistema"}
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <input 
              type="email" 
              className="form-control form-control-lg bg-light border-0" 
              placeholder="Seu e-mail" 
              required 
              value={email} 
              onChange={e => setEmail(e.target.value)} 
            />
          </div>
          
          <div className="mb-3">
            <input 
              type="password" 
              className="form-control form-control-lg bg-light border-0" 
              placeholder="Sua senha" 
              required 
              value={senha} 
              onChange={e => setSenha(e.target.value)} 
            />
          </div>

          <button 
            type="submit" 
            className="btn btn-lg w-100 text-white fw-bold rounded-pill shadow-sm" 
            style={{ backgroundColor: "var(--achei-teal)" }}
            disabled={loading}
          >
            {loading ? "Aguarde..." : (isLogin ? "Entrar no Achei!" : "Criar minha conta")}
          </button>
        </form>
        
        <div className="text-center mt-4">
          <button 
            className="btn btn-link text-decoration-none text-secondary" 
            onClick={() => setIsLogin(!isLogin)}
          >
            {isLogin ? "Ainda não tem conta? Clique aqui" : "Já possui conta? Voltar ao Login"}
          </button>
        </div>

      </div>
    </div>
  );
};

export default Auth;
