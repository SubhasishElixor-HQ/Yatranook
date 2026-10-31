import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { ArrowRight, Check, Compass, LocateFixed, MapPin, Send, Sparkles, Wallet, Users, CalendarDays, MapPinned } from 'lucide-react';
import { PageHeading, Button, AssistantBadge, DestinationCard } from '../components/UI';
import { apiMode, chatTrip, createTripPlan } from '../lib/api/client';
import { useTripStore } from '../store/useTripStore';
import type { TripRequest } from '../types';

const interests = ['Temples', 'Beaches', 'Nature', 'Heritage', 'Wildlife', 'Local food', 'Culture', 'Photography'];

export function PlannerPage() {
  const { request, setRequest } = useTripStore();
  const [origin, setOrigin] = useState(request.origin);
  const [region, setRegion] = useState(request.region);
  const [budget, setBudget] = useState(String(request.budget));
  const [budgetType, setBudgetType] = useState<TripRequest['budgetType']>(request.budgetType);
  const [travelers, setTravelers] = useState(String(request.travelers));
  const [duration, setDuration] = useState<TripRequest['duration']>(request.duration);
  const [selectedInterests, setSelectedInterests] = useState<string[]>(request.interests);
  const [chatText, setChatText] = useState('');
  const [conversation, setConversation] = useState<{ role: 'assistant' | 'user'; text: string }[]>([
    { role: 'assistant', text: 'Hello! I’m here to help shape a journey that fits your time, interests, and budget. Let’s start with where you are.' }
  ]);
  const [error, setError] = useState('');
  const [chatResult, setChatResult] = useState<Awaited<ReturnType<typeof chatTrip>> | null>(null);
  const mutation = useMutation({ mutationFn: createTripPlan, onSuccess: (result) => { setConversation((items) => [...items, { role: 'assistant', text: result.message }]); } });
  const chatMutation = useMutation({
    mutationFn: (input: { message: string; history: { role: 'user' | 'assistant'; content: string }[] }) =>
      chatTrip({ origin: origin.trim(), region: region.trim(), budget: Number(budget) || undefined, budgetType, travelers: Number(travelers) || 1, duration, interests: selectedInterests, ...input }),
    onSuccess: (result) => {
      setChatResult(result);
      setConversation((items) => [...items, { role: 'assistant', text: result.message }]);
    },
  });

  const useCurrentLocation = () => {
    setError('');
    if (!navigator.geolocation) { setError('Location is not available in this browser. Enter your starting place manually.'); return; }
    navigator.geolocation.getCurrentPosition(async (position) => {
      // Coordinates are kept local in this demo. A real reverse-geocoding API should resolve the address.
      setOrigin(`${position.coords.latitude.toFixed(4)}, ${position.coords.longitude.toFixed(4)}`);
      setError('Coordinates captured. Connect a geocoding provider to resolve this into a place name.');
    }, () => setError('Location permission was not granted. You can enter your city or locality manually.'), { timeout: 8000, maximumAge: 60_000 });
  };

  const toggleInterest = (interest: string) => setSelectedInterests((items) => items.includes(interest) ? items.filter((item) => item !== interest) : [...items, interest]);

  const submitPlan = () => {
    const parsedBudget = Number(budget);
    const parsedTravelers = Number(travelers);
    if (!origin.trim()) { setError('Add a starting location to continue.'); return; }
    if (!Number.isFinite(parsedBudget) || parsedBudget <= 0) { setError('Enter a valid positive budget. A small budget is welcome—we will look for practical options.'); return; }
    if (!Number.isInteger(parsedTravelers) || parsedTravelers < 1 || parsedTravelers > 30) { setError('Enter a traveler count between 1 and 30.'); return; }
    const next: TripRequest = { origin: origin.trim(), region: region.trim(), budget: parsedBudget, budgetType, travelers: parsedTravelers, duration, interests: selectedInterests };
    setRequest(next);
    setError('');
    setConversation((items) => [...items, { role: 'user', text: `Plan a ${duration === 'day' ? 'one-day' : duration === 'weekend' ? 'weekend' : 'multi-day'} trip from ${origin} in ${region || 'a place you recommend'}, with ₹${parsedBudget.toLocaleString('en-IN')} ${budgetType === 'total' ? 'total' : 'per person'} for ${parsedTravelers} traveler(s). Interests: ${selectedInterests.join(', ') || 'Open to suggestions'}.` }]);
    mutation.mutate(next);
  };

  const sendMessage = () => {
    const message = chatText.trim();
    if (!message) return;
    const history = conversation.map((item) => ({ role: item.role, content: item.text }));
    setConversation((items) => [...items, { role: 'user', text: message }]);
    setChatText('');
    chatMutation.mutate({ message, history });
  };

  return <div className="page-stack">
    <PageHeading eyebrow="YOUR PERSONAL TRAVEL PLANNER" title="Let’s plan your next journey" description="Start with where you are. We’ll shape the route around your interests, available time, and budget." action={<AssistantBadge/>}/>
    <div className="planner-layout">
      <section className="panel planner-form-panel">
        <div className="panel-heading"><div><span className="step-label">STEP 01 · YOUR JOURNEY</span><h2>Tell us a little about your trip</h2><p>A few details help us make suggestions that feel relevant.</p></div><div className="planner-compass"><Compass size={22}/></div></div>
        <div className="form-grid">
          <div className="form-field span-two"><label htmlFor="origin">Where are you starting from?</label><div className="input-with-action"><MapPin size={17}/><input id="origin" value={origin} onChange={(e) => setOrigin(e.target.value)} placeholder="City, area or landmark"/><button type="button" onClick={useCurrentLocation}><LocateFixed size={15}/> Use current location</button></div><small>We only request your location when you choose to use it.</small></div>
          <div className="form-field span-two"><label htmlFor="region">Where would you like to explore?</label><div className="input-with-icon"><MapPinned size={17}/><input id="region" value={region} onChange={(e) => setRegion(e.target.value)} placeholder="A destination, city, or state — or leave flexible"/></div></div>
          <div className="form-field"><label htmlFor="budget">Your budget (₹)</label><div className="input-with-icon"><Wallet size={16}/><input id="budget" type="number" min="1" step="1" value={budget} onChange={(e) => setBudget(e.target.value)} placeholder="e.g. 1500"/></div></div>
          <div className="form-field"><label>Budget type</label><div className="segmented"><button className={budgetType === 'total' ? 'selected' : ''} onClick={() => setBudgetType('total')}>Total trip</button><button className={budgetType === 'per-person' ? 'selected' : ''} onClick={() => setBudgetType('per-person')}>Per person</button></div></div>
          <div className="form-field"><label htmlFor="travelers">Travelers</label><div className="input-with-icon"><Users size={16}/><input id="travelers" type="number" min="1" max="30" value={travelers} onChange={(e) => setTravelers(e.target.value)}/></div></div>
          <div className="form-field"><label htmlFor="duration">How long?</label><div className="input-with-icon"><CalendarDays size={16}/><select id="duration" value={duration} onChange={(e) => setDuration(e.target.value as TripRequest['duration'])}><option value="day">One day</option><option value="weekend">Weekend</option><option value="multi-day">Several days</option></select></div></div>
          <div className="form-field span-two"><label>What would you love to experience?</label><div className="interest-list">{interests.map((item) => <button key={item} type="button" className={`interest-chip ${selectedInterests.includes(item) ? 'selected' : ''}`} onClick={() => toggleInterest(item)}>{selectedInterests.includes(item) && <Check size={13}/>} {item}</button>)}</div></div>
        </div>
        {error && <div className="inline-alert" role="alert">{error}</div>}
        <div className="planner-form-footer"><span><ShieldCheckIcon/> Your trip preferences stay under your control.</span><Button onClick={submitPlan} disabled={mutation.isPending}>{mutation.isPending ? 'Thinking...' : 'Create my trip plan'} <ArrowRight size={16}/></Button></div>
        {mutation.isError && <p className="error-note">Could not reach the planning service. Check the API connection or use the local preview.</p>}
      </section>
      <aside className="planner-assistant-column">
        <section className="assistant-panel">
          <div className="assistant-panel-head"><div className="assistant-avatar"><Sparkles size={17}/></div><div><strong>Yatranook assistant</strong><small><i/> Ready to help</small></div><span className="assistant-mini-tag">AI PLANNER</span></div>
          <div className="conversation-list">{conversation.map((item, index) => <div key={`${item.role}-${index}`} className={`chat-message ${item.role}`}><div className="chat-bubble">{item.text}</div></div>)}{(mutation.isPending || chatMutation.isPending) && <div className="chat-message assistant"><div className="chat-bubble typing-dots"><i/><i/><i/></div></div>}</div>
          <div className="chat-suggestions"><span>TRY ASKING</span><button onClick={() => setChatText('Find affordable places near my starting point')}>Places near me</button><button onClick={() => setChatText('Make the route cheaper with fewer travel hops')}>Reduce travel cost</button></div>
          <div className="chat-input"><input value={chatText} onChange={(e) => setChatText(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') sendMessage(); }} placeholder="Ask or refine your trip..." aria-label="Message Yatranook"/><button onClick={sendMessage} aria-label="Send message"><Send size={17}/></button></div>
          <div className="demo-caption">{apiMode === 'api' ? 'Connected to the Yatranook planning API · LLM, RAG, routing, and fare capabilities depend on configuration' : 'Local UI preview · Connect FastAPI for backend planning and AI services'}</div>
        </section>
        <div className="planner-tip"><div className="tip-icon"><Sparkles size={17}/></div><div><strong>Small budget? That’s okay.</strong><p>We’ll explore nearby places, affordable transport, and shorter routes before suggesting you increase your budget.</p></div></div>
      </aside>
    </div>
    {mutation.isSuccess && mutation.data.warnings?.map((warning) => <div className="inline-alert" role="status" key={warning}>{warning}</div>)}
    {mutation.isSuccess && mutation.data.sources && mutation.data.sources.length > 0 && <section className="panel"><div className="section-title"><div><span className="eyebrow">RETRIEVED KNOWLEDGE</span><h2>Sources used</h2></div></div><div className="tag-row">{mutation.data.sources.map((source) => <span key={`${source.source_name}-${source.title}`}>{source.source_name}: {source.source_url ? <a href={source.source_url} target="_blank" rel="noreferrer">{source.title}</a> : source.title}</span>)}</div></section>}
    {chatResult?.suggested.length ? <section className="panel"><div className="section-title"><div><span className="eyebrow">CHAT RECOMMENDATIONS</span><h2>Places from this conversation</h2><p>Grounded in the current destination catalogue and retrieved tourism context.</p></div></div><div className="destination-grid">{chatResult.suggested.map((destination) => <DestinationCard key={destination.id} destination={destination}/>)}</div></section> : null}
    {mutation.isSuccess && <section className="planner-results"><div className="section-title"><div><span className="eyebrow">{mutation.data.mode === 'demo' ? 'SAMPLE SUGGESTIONS' : 'DESTINATION MATCHES'}</span><h2>Places to consider</h2><p>{mutation.data.mode === 'demo' ? 'Illustrative options from the local demo dataset, not live availability.' : 'Matches from the current destination catalogue. Verify time-sensitive visitor details before travelling.'}</p></div></div><div className="destination-grid">{mutation.data.suggested.map((destination) => <DestinationCard key={destination.id} destination={destination}/>)}</div></section>}
  </div>;
}

function ShieldCheckIcon() { return <span className="tiny-shield">✓</span>; }
