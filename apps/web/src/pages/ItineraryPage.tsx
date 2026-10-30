import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { ArrowDown, ArrowUp, Clock3, MapPin, Navigation, Plus, Route, Save, Trash2, Wallet } from 'lucide-react';
import { Button, PageHeading, RoutePreview } from '../components/UI';
import { demoStops } from '../data/demo';
import { apiMode, optimizeRoute } from '../lib/api/client';
import { useTripStore } from '../store/useTripStore';
import type { RouteMode } from '../types';

const modes: { id: RouteMode; label: string; detail: string }[] = [
  { id: 'cheapest', label: 'Cheapest', detail: 'Needs real fare data' },
  { id: 'fastest', label: 'Fastest', detail: 'Needs road durations' },
  { id: 'shortest', label: 'Shortest', detail: 'Road distance required' },
  { id: 'balanced', label: 'Balanced', detail: 'Balance time and cost' },
];

export function ItineraryPage() {
  const [stops, setStops] = useState(demoStops);
  const [notice, setNotice] = useState('');
  const [routeInfo, setRouteInfo] = useState<{ status: string; distance: string; duration: string; limitations: string[] } | null>(null);
  const { request, routeMode, setRouteMode, setSavedTrip } = useTripStore();
  const move = (index: number, offset: number) => setStops((items) => { const target = index + offset; if (target < 0 || target >= items.length) return items; const next = [...items]; [next[index], next[target]] = [next[target]!, next[index]!]; return next; });
  const remove = (id: string) => setStops((items) => items.filter((item) => item.id !== id));
  const save = () => { setSavedTrip(true); setNotice('Trip draft saved on this device. Sign in from My Trips to save a trip record to PostgreSQL.'); };
  const routeMutation = useMutation({
    mutationFn: optimizeRoute,
    onSuccess: (result) => {
      const order = new Map(result.ordered_stops.map((stop, index) => [stop.id, index]));
      setStops((current) => [...current].sort((a, b) => (order.get(a.id) ?? Number.MAX_SAFE_INTEGER) - (order.get(b.id) ?? Number.MAX_SAFE_INTEGER)));
      setRouteInfo({
        status: result.status,
        distance: result.road_distance_km != null ? `${result.road_distance_km} km road distance` : `${result.straight_line_distance_km} km straight-line preview`,
        duration: result.duration_minutes != null ? `${result.duration_minutes} min provider duration` : 'Not available',
        limitations: result.limitations,
      });
      setNotice('Stop sequence refreshed using the available route service. Review the limitations before relying on the preview.');
    },
    onError: () => setNotice('Could not optimize this route. Check the API and routing-provider configuration.'),
  });
  const optimize = (mode: RouteMode) => {
    setRouteMode(mode);
    setNotice('');
    if (apiMode !== 'api') { setNotice('Demo mode: route optimization needs the FastAPI backend. The displayed route remains illustrative.'); return; }
    if (!request.origin.toLowerCase().includes('bhubaneswar')) { setNotice('The current draft uses sample stop coordinates for Bhubaneswar. A geocoding provider is required to route from your selected origin.'); return; }
    const validStops = stops.filter((stop) => Number.isFinite(stop.latitude) && Number.isFinite(stop.longitude));
    if (!validStops.length) { setNotice('Add destinations with verified coordinates before optimizing this route.'); return; }
    routeMutation.mutate({
      origin: { id: 'origin', name: request.origin || 'Bhubaneswar, Odisha', latitude: 20.2961, longitude: 85.8245 },
      stops: validStops.map((stop) => ({ id: stop.id, name: stop.name, latitude: stop.latitude!, longitude: stop.longitude! })),
      mode,
    });
  };
  const openDirections = () => {
    const origin = request.origin || 'Bhubaneswar, Odisha';
    const destination = stops.at(-1)?.area || stops.at(-1)?.name || 'Dhauli, Odisha';
    const waypoints = stops.slice(0, -1).map((stop) => stop.area || stop.name).join('|');
    const params = new URLSearchParams({ api: '1', origin, destination, travelmode: 'driving' });
    if (waypoints) params.set('waypoints', waypoints);
    window.open(`https://www.google.com/maps/dir/?${params.toString()}`, '_blank', 'noopener,noreferrer');
  };
  return <div className="page-stack">
    <PageHeading eyebrow="MAKE THE STOPS MAKE SENSE" title="Your route & itinerary" description="Arrange the day around nearby places, realistic timing, and the experience you want." action={<Button variant="secondary" onClick={save}><Save size={16}/> Save trip</Button>}/>
    <div className="itinerary-summary-row"><div className="itinerary-summary-card"><span>YOUR START</span><strong><MapPin size={16}/> {request.origin || 'Bhubaneswar, Odisha'}</strong><small>Origin in current trip context</small></div><div className="itinerary-summary-card"><span>PLANNED STOPS</span><strong><Route size={16}/> {stops.length} places</strong><small>Editable stop sequence</small></div><div className="itinerary-summary-card"><span>TRAVEL STYLE</span><strong><Wallet size={16}/> Budget-aware</strong><small>Fare data required for cost optimization</small></div></div>
    <div className="route-mode-panel"><div><h2>How should we optimize?</h2><p>Choose what matters most for this journey.</p></div><div className="route-mode-options">{modes.map((mode) => <button key={mode.id} onClick={() => optimize(mode.id)} className={`route-mode ${routeMode === mode.id ? 'active' : ''}`} disabled={routeMutation.isPending}><span className="route-mode-radio"/><strong>{mode.label}</strong><small>{mode.detail}</small></button>)}</div></div>
    <div className="itinerary-workspace"><section className="panel route-map-panel"><div className="panel-title-row"><div><h2>Route overview</h2><p>{routeInfo?.status === 'provider_route' ? 'Routing provider response received' : 'Illustrative map preview · map tiles and route geometry not rendered here'}</p></div><span className="sample-tag">{routeMutation.isPending ? 'OPTIMIZING' : routeInfo?.status === 'provider_route' ? 'PROVIDER DATA' : 'PREVIEW'}</span></div><RoutePreview/><div className="map-stats"><div><span>Route distance</span><strong>{routeInfo?.distance || 'Provider required'}</strong></div><div><span>Travel duration</span><strong>{routeInfo?.duration || 'Provider required'}</strong></div><div><span>Stops</span><strong>{stops.length} destinations</strong></div></div>{routeInfo?.limitations.map((item) => <p className="source-note" key={item}>{item}</p>)}<button className="button button-secondary full-width" onClick={openDirections}><Navigation size={16}/> Open directions in Google Maps <ArrowDown size={14}/></button></section>
      <section className="panel stops-panel"><div className="panel-title-row"><div><h2>Your day, stop by stop</h2><p>Reorder or remove stops to shape the journey.</p></div><button className="icon-button" aria-label="Add stop" onClick={() => setNotice('Destination search will let you add an attraction with coordinates after the destination catalogue is connected.')}><Plus size={18}/></button></div><div className="stop-list">{stops.map((stop, index) => <div className="stop-item" key={stop.id}><div className="stop-index-column"><span className="stop-index">{index + 1}</span>{index < stops.length - 1 && <i/>}</div><div className="stop-content"><div className="stop-time">{stop.time} <span>· {stop.duration}</span></div><h3>{stop.name}</h3><div className="stop-area"><MapPin size={13}/>{stop.area}</div><p>{stop.note}</p><small><Clock3 size={12}/>{stop.travel}</small></div><div className="stop-actions"><button aria-label={`Move ${stop.name} up`} disabled={index === 0} onClick={() => move(index, -1)}><ArrowUp size={15}/></button><button aria-label={`Move ${stop.name} down`} disabled={index === stops.length - 1} onClick={() => move(index, 1)}><ArrowDown size={15}/></button><button aria-label={`Remove ${stop.name}`} onClick={() => remove(stop.id)}><Trash2 size={15}/></button></div></div>)}</div><div className="itinerary-end-note"><span className="end-dot"/> End of current draft</div></section></div>
    {notice && <div className="inline-alert success-alert" role="status">{notice}<button onClick={() => setNotice('')} aria-label="Dismiss">×</button></div>}
  </div>;
}
