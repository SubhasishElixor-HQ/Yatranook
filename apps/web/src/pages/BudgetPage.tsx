import { useState } from 'react';
import { Lightbulb, RefreshCw, Wallet } from 'lucide-react';
import { PageHeading, Button } from '../components/UI';
import { demoBudget } from '../data/demo';
import { useTripStore } from '../store/useTripStore';

export function BudgetPage() {
  const { request, setRequest } = useTripStore();
  const initialTripBudget = request.budgetType === 'per-person' ? request.budget * request.travelers : request.budget;
  const [budget, setBudget] = useState(String(initialTripBudget));
  const [optimized, setOptimized] = useState(false);
  const [message, setMessage] = useState('');
  const activeExpenses = optimized ? [
    { label: 'Local transport', amount: 350, color: 'blue' },
    { label: 'Food & refreshments', amount: 400, color: 'teal' },
    { label: 'Entry & activities', amount: 150, color: 'amber' },
    { label: 'Buffer', amount: 150, color: 'slate' },
  ] : demoBudget;
  const total = activeExpenses.reduce((sum, item) => sum + item.amount, 0);
  const budgetValue = Number(budget) > 0 ? Number(budget) : 0;
  const available = budgetValue - total;
  const applyBudget = () => {
    if (!Number.isFinite(budgetValue) || budgetValue <= 0) { setMessage('Enter a positive amount. A low but valid budget is accepted.'); return; }
    setRequest({ budget: budgetValue, budgetType: 'total' }); setMessage('Budget updated in your trip draft. The sample expense breakdown remains illustrative.');
  };
  const optimize = () => { setOptimized((value) => !value); setMessage('Demo budget option toggled. A connected planning API must recalculate route and cost options using real provider data.'); };
  return <div className="page-stack">
    <PageHeading eyebrow="SPEND WITH CLARITY" title="Your trip budget" description="Understand the shape of your spend, set your limit, and explore more affordable choices." action={<span className="sample-tag">ILLUSTRATIVE ESTIMATES</span>}/>
    <section className="budget-hero"><div><div className="budget-hero-label"><Wallet size={15}/> YOUR PLANNING LIMIT</div><div className="budget-hero-amount"><span>₹</span>{(request.budgetType === 'per-person' ? request.budget * request.travelers : request.budget).toLocaleString('en-IN')}</div><p>{request.budgetType === 'total' ? 'Total trip budget' : `₹${request.budget.toLocaleString('en-IN')} per person`} · {request.travelers} traveler(s)</p></div><div className="budget-hero-side"><div className="budget-status"><span className="status-dot"/> Draft estimate</div><span>Estimated sample spend</span><strong>₹{total.toLocaleString('en-IN')}</strong><small>{available >= 0 ? `₹${available.toLocaleString('en-IN')} remaining` : `₹${Math.abs(available).toLocaleString('en-IN')} above this limit`}</small></div></section>
    <div className="budget-layout"><section className="panel budget-breakdown-panel"><div className="panel-title-row"><div><h2>Estimated cost breakdown</h2><p>Example costs for interface demonstration, not live quotes.</p></div><span className="sample-tag">SAMPLE DATA</span></div><div className="budget-bar">{activeExpenses.map((item) => <span key={item.label} className={`budget-segment ${item.color}`} style={{ width: `${item.amount / total * 100}%` }}/>)}</div><div className="budget-legend">{activeExpenses.map((item) => <div key={item.label} className="budget-legend-row"><span className={`legend-dot ${item.color}`}/><span>{item.label}</span><strong>₹{item.amount.toLocaleString('en-IN')}</strong><small>{Math.round(item.amount / total * 100)}%</small></div>)}</div></section>
      <section className="panel budget-edit-panel"><div className="panel-title-row"><div><h2>Adjust your budget</h2><p>There is no arbitrary minimum trip budget.</p></div></div><label htmlFor="budget-limit">Your total budget (₹)</label><input className="budget-edit-input" id="budget-limit" type="number" min="1" value={budget} onChange={(e) => setBudget(e.target.value)}/><div className="budget-quick"><button onClick={() => setBudget('1000')}>₹1,000</button><button onClick={() => setBudget('1500')}>₹1,500</button><button onClick={() => setBudget('2000')}>₹2,000</button><button onClick={() => setBudget('3000')}>₹3,000</button></div><Button className="full-width" onClick={applyBudget}>Update budget</Button></section></div>
    <section className="budget-advice"><div className="advice-icon"><Lightbulb size={19}/></div><div className="advice-copy"><span className="eyebrow">YATRANOOK SUGGESTION</span><h3>{available >= 0 ? 'You have room to shape the experience.' : 'Let’s make this plan more affordable.'}</h3><p>{available >= 0 ? 'Consider keeping a small buffer for local travel or unexpected costs. Actual prices should be checked before booking.' : 'A lower-cost route, fewer stops, or nearby attractions may help. The live planner will compare options when routing and pricing data are connected.'}</p></div><Button variant="secondary" onClick={optimize}><RefreshCw size={15}/> {optimized ? 'Show original estimate' : 'Optimize sample plan'}</Button></section>
    {message && <div className="inline-alert success-alert">{message}<button onClick={() => setMessage('')} aria-label="Dismiss">×</button></div>}
  </div>;
}
