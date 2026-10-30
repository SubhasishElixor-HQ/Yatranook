import { useState, type FormEvent } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { ArrowLeft, Compass, Eye, EyeOff, LockKeyhole, Mail, UserRound } from 'lucide-react';
import { Brand } from '../components/Brand';
import { Button } from '../components/UI';
import { apiMode, getCurrentUser, loginAccount, registerAccount } from '../lib/api/client';
import { useAuthStore } from '../store/useAuthStore';

export function AuthPage({ mode }: { mode: 'login' | 'register' }) {
  const isRegister = mode === 'register';
  const navigate = useNavigate();
  const location = useLocation();
  const setSession = useAuthStore((state) => state.setSession);
  const setAccessToken = useAuthStore((state) => state.setAccessToken);
  const clearSession = useAuthStore((state) => state.clearSession);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError('');
    if (apiMode !== 'api') {
      setError('Connect the FastAPI backend to create an account or sign in. Local demo browsing remains available.');
      return;
    }
    setBusy(true);
    try {
      if (isRegister) await registerAccount({ email, full_name: name, password });
      const token = await loginAccount({ email, password });
      setAccessToken(token.access_token);
      const user = await getCurrentUser();
      setSession(token.access_token, user);
      const next = new URLSearchParams(location.search).get('next');
      navigate(next?.startsWith('/app') ? next : '/app/dashboard', { replace: true });
    } catch (err) {
      clearSession();
      const detail = (err as { response?: { data?: { detail?: string } } }).response?.data?.detail;
      setError(detail || 'Could not complete the request. Check the API connection and try again.');
    } finally {
      setBusy(false);
    }
  };

  return <main className="auth-page">
    <header className="auth-top"><Link to="/" className="back-link"><ArrowLeft size={15}/> Back to Yatranook</Link><Brand/></header>
    <div className="auth-content">
      <section className="auth-story">
        <span className="eyebrow">YOUR JOURNEY, YOUR WAY</span>
        <h1>Every great journey starts with a <em>better plan.</em></h1>
        <p>Keep your travel ideas, preferences, and saved itineraries together as you discover Odisha with Yatranook.</p>
        <div className="auth-story-stat"><div className="auth-story-icon"><Compass size={20}/></div><div><strong>Discover. Plan. Explore.</strong><small>One connected travel-planning workspace.</small></div></div>
      </section>
      <section className="panel auth-card">
        <span className="eyebrow">YATRANOOK ACCOUNT</span>
        <h2>{isRegister ? 'Create your account' : 'Welcome back'}</h2>
        <p>{isRegister ? 'Save your journeys and return to them whenever you are ready.' : 'Sign in to access your saved travel plans.'}</p>
        <form onSubmit={submit} className="auth-form">
          {isRegister && <label>Full name<div className="auth-input"><UserRound size={16}/><input value={name} onChange={(e) => setName(e.target.value)} required minLength={2} maxLength={160} autoComplete="name" placeholder="Your name"/></div></label>}
          <label>Email address<div className="auth-input"><Mail size={16}/><input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required autoComplete="email" placeholder="you@example.com"/></div></label>
          <label>Password<div className="auth-input"><LockKeyhole size={16}/><input type={showPassword ? 'text' : 'password'} value={password} onChange={(e) => setPassword(e.target.value)} required minLength={isRegister ? 12 : 1} maxLength={128} autoComplete={isRegister ? 'new-password' : 'current-password'} placeholder={isRegister ? 'At least 12 characters' : 'Enter your password'}/><button type="button" aria-label={showPassword ? 'Hide password' : 'Show password'} onClick={() => setShowPassword((value) => !value)}>{showPassword ? <EyeOff size={16}/> : <Eye size={16}/>}</button></div></label>
          {error && <div className="inline-alert" role="alert">{error}</div>}
          <Button type="submit" className="full-width" disabled={busy}>{busy ? 'Please wait…' : isRegister ? 'Create account' : 'Sign in'}</Button>
        </form>
        <div className="auth-switch">{isRegister ? 'Already have an account?' : 'New to Yatranook?'} <Link to={isRegister ? '/login' : '/register'}>{isRegister ? 'Sign in' : 'Create account'}</Link></div>
        <small className="auth-note">Account registration uses the configured API. Passwords are never stored in the browser.</small>
      </section>
    </div>
  </main>;
}
