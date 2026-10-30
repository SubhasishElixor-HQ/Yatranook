import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { CalendarDays, MapPin, Plus, ArrowUpRight, Bookmark, Clock3 } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { PageHeading } from '../components/UI';
import { apiMode, listSavedTrips, saveTrip } from '../lib/api/client';
import { useAuthStore } from '../store/useAuthStore';
import { useTripStore } from '../store/useTripStore';

export function TripsPage() {
  const { request, savedTrip, setSavedTrip } = useTripStore();
  const token = useAuthStore((state) => state.accessToken);
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState('All trips');
  const tripsQuery = useQuery({ queryKey: ['saved-trips'], queryFn: listSavedTrips, enabled: apiMode === 'api' && Boolean(token), retry: false });
  const saveMutation = useMutation({
    mutationFn: () => saveTrip(request),
    onSuccess: async () => { setSavedTrip(true); await queryClient.invalidateQueries({ queryKey: ['saved-trips'] }); },
  });
  const handleSave = () => {
    if (apiMode === 'api') {
      if (!token) { navigate('/login?next=/app/trips'); return; }
      saveMutation.mutate();
    } else setSavedTrip(true);
  };
  const remoteTrips = tripsQuery.data ?? [];
  const visibleRemoteTrips = activeTab === 'All trips' ? remoteTrips : remoteTrips.filter((trip) => trip.status.toLowerCase() === activeTab.toLowerCase().replace(' trips', ''));
  const showDraft = activeTab === 'All trips' ? !(apiMode === 'api' && savedTrip) : activeTab === 'Drafts' && !savedTrip;

  return <div className="page-stack">
    <PageHeading eyebrow="YOUR JOURNEYS, ALL IN ONE PLACE" title="My trips" description="Keep your ideas, drafts, and saved journeys easy to return to." action={<Link to="/app/planner" className="button button-primary"><Plus size={16}/> Create a trip</Link>}/>
    <div className="trip-tabs">{[['All trips', remoteTrips.length + (savedTrip ? 0 : 1)], ['Upcoming', 0], ['Completed', 0], ['Drafts', savedTrip ? 0 : 1]].map(([label, count]) => <button key={String(label)} onClick={() => setActiveTab(String(label))} className={activeTab === label ? 'active' : ''}>{label} <span>{count}</span></button>)}</div>
    {visibleRemoteTrips.map((trip) => <section className="trip-list-card" key={trip.id}>
      <div className="trip-cover"><img src="https://images.unsplash.com/photo-1606293926075-69a00dbfde81?auto=format&fit=crop&w=1000&q=85" alt="Indian heritage architecture"/><span className="trip-cover-tag">SAVED TRIP</span></div>
      <div className="trip-card-content"><div className="trip-card-top"><span className="status-label"><i/> {trip.status.toUpperCase()}</span><span className="sample-tag">SYNCED TO ACCOUNT</span></div><h2>{trip.title}</h2><p>A saved journey beginning from {trip.origin}.</p><div className="trip-detail-row"><span><MapPin size={14}/>{trip.origin}</span><span><CalendarDays size={14}/>{trip.duration}</span><span><Clock3 size={14}/>{trip.travelers} traveler(s)</span></div><div className="trip-card-bottom"><div><small>PLANNING BUDGET</small><strong>₹{Number(trip.budget).toLocaleString('en-IN')}</strong></div><span className="text-link">Saved {new Date(trip.created_at).toLocaleDateString('en-IN')}</span></div></div>
    </section>)}
    {showDraft && <section className="trip-list-card">
      <div className="trip-cover"><img src="https://images.unsplash.com/photo-1606293926075-69a00dbfde81?auto=format&fit=crop&w=1000&q=85" alt="Indian heritage architecture"/><span className="trip-cover-tag">ODISHA · PLANNING DRAFT</span></div>
      <div className="trip-card-content"><div className="trip-card-top"><span className="status-label"><i/> {savedTrip ? 'SAVED ON THIS DEVICE' : 'PLANNING DRAFT'}</span><button className="icon-button" aria-label="Save trip" onClick={handleSave} disabled={saveMutation.isPending}><Bookmark size={17}/></button></div><h2>{request.region || 'Odisha'} exploration</h2><p>A flexible trip draft beginning from {request.origin || 'your selected location'}.</p><div className="trip-detail-row"><span><MapPin size={14}/>{request.origin || 'Starting point not set'}</span><span><CalendarDays size={14}/>{request.duration === 'day' ? 'One day' : request.duration === 'weekend' ? 'Weekend' : 'Multi-day'}</span><span><Clock3 size={14}/>Dates not selected</span></div><div className="trip-card-bottom"><div><small>PLANNING BUDGET</small><strong>₹{request.budget.toLocaleString('en-IN')}</strong></div><Link className="button button-secondary" to="/app/itinerary">Open itinerary <ArrowUpRight size={15}/></Link></div>
      {saveMutation.isError && <p className="error-note">Could not save this trip. Check your session and API connection.</p>}
      </div>
    </section>}
    {tripsQuery.isError && <div className="inline-alert" role="alert">Could not load account trips. You may need to sign in again.</div>}
    {apiMode === 'api' && !token && <div className="trip-disclaimer"><Bookmark size={17}/> <span>Sign in to synchronize trip records with your account. Your current planning draft stays in this browser.</span> <Link to="/login?next=/app/trips" className="text-link">Sign in <ArrowUpRight size={14}/></Link></div>}
    {apiMode === 'demo' && <div className="trip-disclaimer"><Bookmark size={17}/><span>Demo mode: trip drafts are stored in this browser. Configure the FastAPI backend and sign in to save trips to PostgreSQL.</span></div>}
    {visibleRemoteTrips.length === 0 && !showDraft && <div className="empty-state"><MapPin size={24}/><h3>No {activeTab.toLowerCase()} yet</h3><p>Your {activeTab.toLowerCase()} will appear here when you create and save a trip.</p><Link className="text-link" to="/app/planner">Plan a journey <ArrowUpRight size={14}/></Link></div>}
    <div className="create-trip-empty"><div className="empty-compass"><Plus size={22}/></div><h3>Your next journey starts here</h3><p>Create another trip draft and explore somewhere new.</p><Link to="/app/planner" className="text-link">Start a new plan <ArrowUpRight size={15}/></Link></div>
  </div>;
}

