import { Bookmark, Compass } from 'lucide-react';
import { Link } from 'react-router-dom';
import { DestinationCard, PageHeading } from '../components/UI';
import { destinations } from '../data/demo';
import { useTripStore } from '../store/useTripStore';

export function SavedPlacesPage() {
  const savedIds = useTripStore((state) => state.savedDestinationIds);
  const saved = destinations.filter((destination) => savedIds.includes(destination.id));
  return <div className="page-stack">
    <PageHeading eyebrow="YOUR PERSONAL COLLECTION" title="Saved places" description="Keep the destinations that caught your eye and bring them into a trip when you’re ready." action={<Link className="button button-secondary" to="/app/explore"><Compass size={16}/> Explore places</Link>}/>
    {saved.length ? <div className="destination-grid">{saved.map((destination) => <DestinationCard key={destination.id} destination={destination}/>)}</div> : <div className="empty-state"><Bookmark size={27}/><h3>Your saved places will appear here</h3><p>Use the bookmark on a destination card to keep a place in your collection.</p><Link className="button button-primary" to="/app/explore">Discover destinations <Compass size={15}/></Link></div>}
    <div className="trip-disclaimer">Saved destinations are stored locally in this browser prototype. Connect user accounts and a saved-places API for multi-device synchronization.</div>
  </div>;
}
