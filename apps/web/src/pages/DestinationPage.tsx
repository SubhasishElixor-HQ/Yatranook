import { Link, useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, ArrowUpRight, Clock3, MapPin, Plus, Sparkles } from 'lucide-react';
import { destinations } from '../data/demo';
import { Button, RoutePreview } from '../components/UI';
import { useTripStore } from '../store/useTripStore';

export function DestinationPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const destination = destinations.find((item) => item.id === id) ?? destinations[0]!;
  const { setRequest } = useTripStore();
  return <div className="page-stack"><Link to="/app/explore" className="back-link"><ArrowLeft size={15}/> Back to Explore</Link>
    <div className="destination-detail-hero"><img src={destination.image} alt={destination.name}/><div className="destination-detail-overlay"><span className="category-pill">{destination.category}</span><h1>{destination.name}</h1><span><MapPin size={15}/>{destination.location}</span></div></div>
    <div className="destination-detail-grid"><section className="panel destination-about"><div className="eyebrow">ABOUT THIS PLACE</div><h2>A place to explore at your own pace.</h2><p>{destination.description} This page uses sample catalogue content. Check official visitor information and current access details before travelling.</p><div className="detail-meta-row"><span><Clock3 size={15}/> Suggested visit: {destination.duration}</span><span><MapPin size={15}/> {destination.distanceKm} km from sample origin*</span></div><div className="tag-row">{destination.tags.map((tag) => <span key={tag}>{tag}</span>)}</div><div className="source-note">Visitor fees, timings, access rules, and live route data have not been verified in this demo.</div><Button onClick={() => { setRequest({ region: destination.name, interests: [destination.category] }); navigate('/app/planner'); }}><Plus size={16}/> Add to trip draft</Button> <Link className="text-link" to="/app/planner">Plan around this place <ArrowUpRight size={15}/></Link></section>
      <aside className="panel destination-side"><div className="panel-title-row"><div><h2>Find your way</h2><p>Illustrative map preview</p></div><Sparkles size={18} className="muted-icon"/></div><RoutePreview compact/><p className="source-note">A connected routing provider is needed for verified road directions and travel times.</p><a className="button button-secondary full-width" href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(destination.name + ', Odisha')}`} target="_blank" rel="noreferrer">Find on Google Maps <ArrowUpRight size={15}/></a></aside></div>
  </div>;
}
