import type { ButtonHTMLAttributes, ComponentType, ReactNode } from 'react';
import { ArrowUpRight, MapPin, Clock3, Bookmark, Sparkles, ArrowRight, Route } from 'lucide-react';
import { Link } from 'react-router-dom';
import type { Destination } from '../types';
import { useTripStore } from '../store/useTripStore';

export function PageHeading({ eyebrow, title, description, action }: { eyebrow?: string; title: string; description?: string; action?: ReactNode }) {
  return <div className="page-heading"><div>{eyebrow && <div className="eyebrow">{eyebrow}</div>}<h1>{title}</h1>{description && <p>{description}</p>}</div>{action && <div className="heading-action">{action}</div>}</div>;
}

export function Button({ children, variant = 'primary', className = '', ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'secondary' | 'ghost' | 'soft' }) {
  return <button className={`button button-${variant} ${className}`} {...props}>{children}</button>;
}

export function DestinationCard({ destination, compact = false }: { destination: Destination; compact?: boolean }) {
  const { setRequest, savedDestinationIds, toggleSavedDestination } = useTripStore();
  const isSaved = savedDestinationIds.includes(destination.id);
  return (
    <article className={`destination-card ${compact ? 'destination-card-compact' : ''}`}>
      <div className="destination-image-wrap"><img src={destination.image} alt={destination.name} loading="lazy" /><span className="category-pill">{destination.category}</span><button className={`save-icon ${isSaved ? 'is-saved' : ''}`} aria-label={`${isSaved ? 'Remove saved' : 'Save'} ${destination.name}`} aria-pressed={isSaved} onClick={() => toggleSavedDestination(destination.id)}><Bookmark size={16}/></button></div>
      <div className="destination-card-body">
        <div className="destination-location"><MapPin size={13}/>{destination.location}</div>
        <h3><Link to={`/app/destinations/${destination.id}`}>{destination.name}</Link></h3>
        <p>{destination.description}</p>
        <div className="destination-meta"><span><Clock3 size={13}/>{destination.duration}</span>{destination.distanceKm && <span><Route size={13}/>{destination.distanceKm} km* (sample)</span>}</div>
        <div className="destination-card-bottom"><span className="price-note">{destination.priceLabel}</span><Link to="/app/planner" onClick={() => setRequest({ region: destination.name, interests: [destination.category] })} className="text-link">Plan around this <ArrowUpRight size={15}/></Link></div>
      </div>
    </article>
  );
}

export function StatCard({ label, value, detail, icon: Icon, tone = 'blue' }: { label: string; value: string; detail: string; icon: ComponentType<{ size?: number }>; tone?: string }) {
  return <div className="stat-card"><div className={`stat-icon tone-${tone}`}><Icon size={19}/></div><div className="stat-copy"><span>{label}</span><strong>{value}</strong><small>{detail}</small></div></div>;
}

export function RoutePreview({ compact = false }: { compact?: boolean }) {
  return (
    <div className={`route-preview ${compact ? 'route-preview-compact' : ''}`}>
      <div className="map-water water-one"/><div className="map-water water-two"/>
      <div className="map-grid"/>
      <svg className="map-path-svg" viewBox="0 0 600 300" preserveAspectRatio="none" aria-label="Illustrative route between planned stops">
        <path d="M78 228 C140 190 166 184 222 164 S320 114 360 126 S445 75 518 57" fill="none" stroke="#ffffff" strokeWidth="10" strokeLinecap="round"/>
        <path d="M78 228 C140 190 166 184 222 164 S320 114 360 126 S445 75 518 57" fill="none" stroke="#2878d0" strokeWidth="4" strokeDasharray="8 7" strokeLinecap="round"/>
      </svg>
      <div className="map-road road-a"/><div className="map-road road-b"/><div className="map-road road-c"/>
      <span className="map-place place-a">Bhubaneswar</span><span className="map-place place-b">Dhauli</span><span className="map-place place-c">Old Town</span>
      <span className="map-marker marker-a">1</span><span className="map-marker marker-b">2</span><span className="map-marker marker-c">3</span>
      <span className="map-compass">N ↑</span><span className="map-scale">Illustrative route preview</span>
      <div className="map-floating-card"><span className="map-live-dot"/> Route concept <strong>3 stops</strong></div>
    </div>
  );
}

export function SectionTitle({ title, subtitle, link }: { title: string; subtitle?: string; link?: string }) {
  return <div className="section-title"><div><h2>{title}</h2>{subtitle && <p>{subtitle}</p>}</div>{link && <Link to={link} className="text-link">View all <ArrowRight size={15}/></Link>}</div>;
}

export function AssistantBadge() { return <span className="assistant-badge"><Sparkles size={13}/> AI ASSISTED</span>; }
