import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Search, Compass, ArrowUpRight, MapPin } from 'lucide-react';
import { Link, useSearchParams } from 'react-router-dom';
import { destinations } from '../data/demo';
import { DestinationCard, PageHeading } from '../components/UI';
import { apiMode, searchDestinations } from '../lib/api/client';

const categories = ['All places', 'Temple', 'Beach', 'Nature', 'Heritage', 'Wildlife', 'Food', 'Culture'];

export function ExplorePage() {
  const [searchParams] = useSearchParams();
  const [query, setQuery] = useState(searchParams.get('q') ?? '');
  const [category, setCategory] = useState('All places');
  const [nearbyOnly, setNearbyOnly] = useState(false);
  const destinationQuery = useQuery({ queryKey: ['destinations', query], queryFn: () => searchDestinations(query), placeholderData: apiMode === 'demo' ? destinations : undefined });
  const sourceItems = destinationQuery.data ?? (apiMode === 'demo' ? destinations : []);
  const filtered = useMemo(() => sourceItems.filter((item) => (category === 'All places' || item.category.toLowerCase() === category.toLowerCase()) && (!nearbyOnly || (item.distanceKm !== undefined && item.distanceKm <= 20)) && `${item.name} ${item.location} ${item.description} ${item.tags.join(' ')}`.toLowerCase().includes(query.toLowerCase())), [sourceItems, query, category, nearbyOnly]);
  return <div className="page-stack">
    <PageHeading eyebrow="FIND YOUR NEXT EXPERIENCE" title="Explore Odisha" description="From living heritage to quiet natural landscapes, find places that match the way you want to travel." action={<Link className="button button-secondary" to="/app/planner"><Compass size={16}/> Plan around a place</Link>}/>
    <section className="explore-hero"><div className="explore-hero-copy"><span className="eyebrow">A REGION OF MANY STORIES</span><h2>Find a place<br/>that stays with you.</h2><p>Search by place, feeling, or experience. Start with a popular destination or follow your curiosity.</p><div className="explore-search"><Search size={18}/><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Try ‘beach’, ‘temple’, or ‘nature’..."/><button aria-label="Apply search" onClick={() => setQuery(query.trim())}><ArrowUpRight size={17}/></button></div></div><div className="explore-hero-image"><img src="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1000&q=85" alt="Green natural landscape"/><div className="explore-image-caption"><MapPin size={14}/> Odisha, India</div></div></section>
    <div className="filter-row"><div className="category-filters">{categories.map((item) => <button key={item} className={`filter-chip ${category === item ? 'active' : ''}`} onClick={() => setCategory(item)}>{item}</button>)}</div><button className={`filter-action ${nearbyOnly ? 'active' : ''}`} onClick={() => setNearbyOnly((value) => !value)}><MapPin size={15}/> {nearbyOnly ? 'Nearby only' : 'Nearby'}</button></div>
    <div className="explore-results-heading"><div><h2>{filtered.length} places to explore</h2><p>{apiMode === 'demo' ? 'Sample destination catalogue · Confirm visitor details before travel' : 'Results from your configured destination API'}</p></div><span className="sort-label">Curated for discovery</span></div>
    {destinationQuery.isLoading && <div className="empty-state">Loading destination results…</div>}
    {destinationQuery.isError && <div className="inline-alert">Could not load destinations from FastAPI. Check the API contract and server availability.</div>}
    {filtered.length ? <div className="destination-grid explore-grid">{filtered.map((destination) => <DestinationCard key={destination.id} destination={destination}/>)}</div> : <div className="empty-state"><Search size={26}/><h3>No places match that search</h3><p>Try another destination name or choose a different category.</p><button className="button button-secondary" onClick={() => { setQuery(''); setCategory('All places'); }}>Clear filters</button></div>}
  </div>;
}
