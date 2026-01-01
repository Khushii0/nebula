import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import ProjectPage from './pages/ProjectPage';

// Configure axios base URL
axios.defaults.baseURL = 'http://localhost:8000';
axios.defaults.headers.common['Content-Type'] = 'application/json';

interface User {
  id: number;
  email: string;
  name: string;
}

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      try {
        const response = await axios.get('/auth/me');
        setUser(response.data);
      } catch (err: any) {
        // Token invalid or expired
        localStorage.removeItem('token');
        delete axios.defaults.headers.common['Authorization'];
        if (err.code === 'ERR_NETWORK') {
          console.error('Backend not reachable. Make sure backend is running on http://localhost:8000');
        }
      }
    }
    setIsLoading(false);
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const response = await axios.post('/auth/login/json', { email, password });
      localStorage.setItem('token', response.data.access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
      setUser({ id: response.data.user_id, email: response.data.email, name: response.data.name || '' });
      setShowLogin(false);
      setEmail('');
      setPassword('');
    } catch (err: any) {
      if (err.code === 'ERR_NETWORK') {
        setError('Cannot connect to backend. Make sure backend is running on http://localhost:8000');
      } else {
        setError(err.response?.data?.detail || 'Login failed');
      }
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    // #region agent log
    fetch('http://127.0.0.1:7242/ingest/1f6aa282-e684-4e49-8547-efec0e407c62',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'App.tsx:handleRegister:entry',message:'Register attempt started',data:{email,hasPassword:!!password,hasName:!!name,baseURL:axios.defaults.baseURL},timestamp:Date.now(),sessionId:'debug-session',runId:'register-attempt',hypothesisId:'NETWORK'})}).catch(()=>{});
    // #endregion
    try {
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/1f6aa282-e684-4e49-8547-efec0e407c62',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'App.tsx:handleRegister:before-request',message:'About to send register request',data:{url:'/auth/register',method:'POST'},timestamp:Date.now(),sessionId:'debug-session',runId:'register-attempt',hypothesisId:'NETWORK'})}).catch(()=>{});
      // #endregion
      const response = await axios.post('/auth/register', { email, password, name });
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/1f6aa282-e684-4e49-8547-efec0e407c62',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'App.tsx:handleRegister:success',message:'Register request succeeded',data:{status:response.status,hasToken:!!response.data.access_token},timestamp:Date.now(),sessionId:'debug-session',runId:'register-attempt',hypothesisId:'NETWORK'})}).catch(()=>{});
      // #endregion
      localStorage.setItem('token', response.data.access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
      setUser({ id: response.data.user_id, email: response.data.email, name: name || response.data.email.split('@')[0] });
      setShowRegister(false);
      setEmail('');
      setPassword('');
      setName('');
    } catch (err: any) {
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/1f6aa282-e684-4e49-8547-efec0e407c62',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'App.tsx:handleRegister:error',message:'Register request failed',data:{errorCode:err.code,errorMessage:err.message,responseStatus:err.response?.status,responseData:err.response?.data,hasResponse:!!err.response,networkError:err.code==='ERR_NETWORK'},timestamp:Date.now(),sessionId:'debug-session',runId:'register-attempt',hypothesisId:'NETWORK'})}).catch(()=>{});
      // #endregion
      if (err.code === 'ERR_NETWORK') {
        setError('Cannot connect to backend. Make sure backend is running on http://localhost:8000');
      } else {
        setError(err.response?.data?.detail || 'Registration failed');
      }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
  };

  if (isLoading) {
    return <div className="App">Loading...</div>;
  }

  if (!user) {
    return (
      <div className="App">
        <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px' }}>
          <h1>Architectural Design Assistant</h1>
          
          {!showLogin && !showRegister && (
            <div>
              <button onClick={() => { setShowLogin(true); setShowRegister(false); setError(''); }}>
                Login
              </button>
              <button onClick={() => { setShowRegister(true); setShowLogin(false); setError(''); }}>
                Register
              </button>
            </div>
          )}

          {showLogin && (
            <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <h2>Login</h2>
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              {error && <div style={{ color: 'red' }}>{error}</div>}
              <button type="submit">Login</button>
              <button type="button" onClick={() => { setShowLogin(false); setError(''); }}>
                Cancel
              </button>
            </form>
          )}

          {showRegister && (
            <form onSubmit={handleRegister} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <h2>Register</h2>
              <input
                type="text"
                placeholder="Name (optional)"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              {error && <div style={{ color: 'red' }}>{error}</div>}
              <button type="submit">Register</button>
              <button type="button" onClick={() => { setShowRegister(false); setError(''); }}>
                Cancel
              </button>
            </form>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <header style={{ padding: '10px 20px', background: '#f0f0f0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Architectural Design Assistant</h1>
        <div>
          <span style={{ marginRight: '20px' }}>Welcome, {user.name || user.email}</span>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </header>
      <main>
        <ProjectPage />
      </main>
    </div>
  );
}

export default App;
