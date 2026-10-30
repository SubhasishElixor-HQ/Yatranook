import { Compass } from 'lucide-react';

export function Brand({ compact = false }: { compact?: boolean }) {
  return (
    <div className="brand-lockup">
      <span className="brand-mark"><Compass size={20} strokeWidth={2.4} /></span>
      {!compact && <span className="brand-name">yatra<span>nook</span><small>TRAVEL, THOUGHTFULLY</small></span>}
    </div>
  );
}
