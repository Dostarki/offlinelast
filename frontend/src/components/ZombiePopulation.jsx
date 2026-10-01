import { useEffect, useState } from 'react';
import { Bug } from 'lucide-react';

const PRESETS = { off: 0, low: 120, normal: 250, high: 450 };

export const ZombiePopulation = ({ settings, save, busy }) => {
  const [count, setCount] = useState(settings.zombie_count);
  useEffect(() => setCount(settings.zombie_count), [settings.zombie_count]);
  const apply = value => {
    const n = Math.max(0, Math.min(600, Math.round(Number(value) || 0)));
    save({ ...settings, zombie_count: n, zombie_density: n === 0 ? 'off' : settings.zombie_density === 'off' ? 'normal' : settings.zombie_density });
  };
  return <div className="admin-density">
    <span className="admin-field-label" data-testid="admin-density-label"><Bug size={14} /> ZOMBIE POPULATION (SERVER-WIDE)</span>
    <select value={settings.zombie_density} disabled={busy} data-testid="admin-zombie-density" onChange={e => save({ ...settings, zombie_density: e.target.value, zombie_count: PRESETS[e.target.value] })}>
      <option value="off">Off (0)</option><option value="low">Low (120)</option><option value="normal">Normal (250)</option><option value="high">High (450)</option>
    </select>
    <div className="admin-bot-input-row admin-zombie-count-row">
      <input type="number" min="0" max="600" value={count} disabled={busy} aria-label="Zombie count" data-testid="admin-zombie-count-input" onChange={e => setCount(e.target.value)} onKeyDown={e => e.key === 'Enter' && apply(count)} />
      <button type="button" className="admin-apply" disabled={busy} data-testid="admin-zombie-count-apply" onClick={() => apply(count)}>APPLY</button>
    </div>
    <p className="admin-zombie-hint" data-testid="admin-zombie-hint">Fixed total for the whole server (0–600), spread evenly across 64 map regions. Players joining do not add zombies.</p>
  </div>;
};
