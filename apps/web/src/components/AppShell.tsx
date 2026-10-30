import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom';
import { Bell, Compass, LayoutDashboard, Map, MapPinned, MessageCircle, Search, Settings, Bookmark, BriefcaseBusiness, Menu, Sparkles, LogOut, UserRound } from 'lucide-react';
import { useState } from 'react';
import { Brand } from './Brand';
import { useAuthStore } from '../store/useAuthStore';

const links = [
  { to: '/app/dashboard', label: 'Overview', icon: LayoutDashboard },
  { to: '/app/planner', label: 'AI trip planner', icon: MessageCircle },
  { to: '/app/explore', label: 'Explore Odisha', icon: Compass },
  { to: '/app/itinerary', label: 'Route & itinerary', icon: MapPinned },
  { to: '/app/budget', label: 'Budget planner', icon: BriefcaseBusiness },
  { to: '/app/trips', label: 'My trips', icon: Map },
];

const titleByPath: Record<string, string> = {
  '/app/dashboard': 'Overview', '/app/planner': 'AI trip planner', '/app/explore': 'Explore Odisha',
  '/app/itinerary': 'Route & itinerary', '/app/budget': 'Budget planner', '/app/trips': 'My trips', '/app/saved': 'Saved places', '/app/settings': 'Settings'
};

export function AppShell() {
  const location = useLocation();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [mobileOpen, setMobileOpen] = useState(false);
  const user = useAuthStore((state) => state.user);
  const clearSession = useAuthStore((state) => state.clearSession);
  const title = titleByPath[location.pathname] ?? 'Yatranook';
  return (
    <div className="app-shell">
      {mobileOpen && <button className="mobile-backdrop" aria-label="Close navigation" onClick={() => setMobileOpen(false)} />}
      <aside className={`sidebar ${mobileOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-brand"><Brand /></div>
        <div className="workspace-label">WORKSPACE</div>
        <nav className="side-nav" aria-label="Main navigation">
          {links.map(({ to, label, icon: Icon }) => (
            <NavLink key={to} to={to} onClick={() => setMobileOpen(false)} className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
              <Icon size={18} /><span>{label}</span>{label === 'AI trip planner' && <span className="nav-new">AI</span>}
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-divider" />
        <div className="workspace-label">YOUR SPACE</div>
        <NavLink to="/app/saved" className="nav-link"><Bookmark size={18}/><span>Saved places</span></NavLink>
        <NavLink to="/app/settings" className="nav-link"><Settings size={18}/><span>Settings</span></NavLink>
        <div className="sidebar-bottom">
          <div className="help-card">
            <div className="help-icon"><Sparkles size={17}/></div>
            <strong>Travel with clarity</strong>
            <p>Your preferences stay with your trip draft on this device.</p>
            <NavLink to="/app/planner">Start planning <span>→</span></NavLink>
          </div>
          <div className="profile-mini">
            <div className="avatar">{user ? user.full_name.slice(0, 2).toUpperCase() : 'YN'}</div>
            <div><strong>{user?.full_name || 'Guest explorer'}</strong><small>{user?.email || 'Local planning workspace'}</small></div>
            {user ? <button className="icon-button" aria-label="Sign out" title="Sign out" onClick={clearSession}><LogOut size={15}/></button> : <button className="icon-button" aria-label="Sign in" title="Sign in" onClick={() => navigate('/login')}><UserRound size={15}/></button>}
          </div>
        </div>
      </aside>
      <div className="app-main">
        <header className="topbar">
          <div className="topbar-left">
            <button className="icon-button mobile-menu" aria-label="Open navigation" onClick={() => setMobileOpen(true)}><Menu size={20}/></button>
            <div className="breadcrumb"><span>Workspace</span><span className="crumb-sep">/</span><strong>{title}</strong></div>
          </div>
          <div className="topbar-actions">
            <label className="top-search"><Search size={16}/><input aria-label="Search Yatranook" value={searchQuery} onChange={(event) => setSearchQuery(event.target.value)} onKeyDown={(event) => { if (event.key === 'Enter' && searchQuery.trim()) navigate(`/app/explore?q=${encodeURIComponent(searchQuery.trim())}`); }} placeholder="Search destinations, trips..." /><kbd>⌘ K</kbd></label>
            <button className="icon-button notification-button" aria-label="Notifications"><Bell size={18}/><i /></button>
            <button className="top-avatar" aria-label={user ? 'Open profile settings' : 'Sign in'} onClick={() => user ? navigate('/app/settings') : navigate('/login')}>{user ? user.full_name.slice(0, 2).toUpperCase() : 'EX'}</button>
          </div>
        </header>
        <main className="page-content"><Outlet /></main>
        <footer className="app-footer"><span>© 2026 Yatranook</span><span>Travel thoughtfully · Odisha first</span></footer>
      </div>
    </div>
  );
}
