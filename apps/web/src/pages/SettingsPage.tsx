import { useState } from 'react';
import { Bell, Globe2, LockKeyhole, UserRound, ShieldCheck, Save } from 'lucide-react';
import { PageHeading, Button } from '../components/UI';

export function SettingsPage() {
  const [name, setName] = useState('Explorer');
  const [language, setLanguage] = useState('English');
  const [currency, setCurrency] = useState('INR · ₹');
  const [saved, setSaved] = useState(false);
  const [locationEnabled, setLocationEnabled] = useState(false);
  return <div className="page-stack">
    <PageHeading eyebrow="MAKE YATRANOOK YOURS" title="Settings & preferences" description="Manage how you plan, what you prefer, and the information you choose to share."/>
    <div className="settings-layout"><nav className="settings-nav"><a className="active" href="#profile"><UserRound size={16}/> Profile</a><a href="#preferences"><Globe2 size={16}/> Preferences</a><a href="#privacy"><LockKeyhole size={16}/> Privacy & permissions</a><a href="#notifications"><Bell size={16}/> Notifications</a></nav>
      <div className="settings-content"><section className="panel settings-panel" id="profile"><div className="settings-section-heading"><div className="settings-icon"><UserRound size={18}/></div><div><h2>Profile</h2><p>Basic information for your travel workspace.</p></div></div><div className="settings-form"><label>Display name<input value={name} onChange={(e) => setName(e.target.value)}/></label><label>Email address<input value="Not connected" disabled/></label></div></section>
        <section className="panel settings-panel" id="preferences"><div className="settings-section-heading"><div className="settings-icon"><Globe2 size={18}/></div><div><h2>Travel preferences</h2><p>Choose defaults for new trip plans.</p></div></div><div className="settings-form two-col"><label>Preferred language<select value={language} onChange={(e) => setLanguage(e.target.value)}><option>English</option><option>Odia</option><option>Hindi</option></select></label><label>Currency<select value={currency} onChange={(e) => setCurrency(e.target.value)}><option>INR · ₹</option><option>USD · $</option></select></label></div></section>
        <section className="panel settings-panel" id="privacy"><div className="settings-section-heading"><div className="settings-icon"><ShieldCheck size={18}/></div><div><h2>Privacy & permissions</h2><p>Location is requested only when you choose to use it.</p></div></div><div className="permission-row"><div><strong>Use current location</strong><p>Allow the browser to provide your location when you request nearby suggestions.</p></div><button className={`toggle ${locationEnabled ? 'on' : ''}`} onClick={() => setLocationEnabled((value) => !value)} aria-label="Toggle location preference"><i/></button></div><div className="permission-row"><div><strong>Saved trip preferences</strong><p>Trip draft preferences are stored locally in this browser in this prototype.</p></div><span className="sample-tag">LOCAL</span></div></section>
        <div className="settings-save"><span>{saved ? 'Preferences updated in this session.' : 'Changes are local to this prototype.'}</span><Button onClick={() => setSaved(true)}><Save size={15}/> Save preferences</Button></div>
      </div>
    </div>
  </div>;
}
