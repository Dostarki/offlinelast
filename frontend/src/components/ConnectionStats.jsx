import { useEffect, useState } from 'react';
import './ConnectionStats.css';

export const ConnectionStats = ({ state, ping, engine }) => {
  const [stats, setStats] = useState({ fps: null, stale: false });
  useEffect(() => {
    const update = () => {
      const game = engine.current;
      setStats({ fps: game?.metrics.fps || null, stale: !!game?.lastReceivedAt && performance.timeOrigin + performance.now() - game.lastReceivedAt > 1500 });
    };
    update(); const timer = setInterval(update, 1000); return () => clearInterval(timer);
  }, [engine]);
  const delayed = ping !== null && ping >= 200;
  return <div className="connection-stats" data-testid="hud-connection">
    <div className="connection-values">
      <i className={`status-dot ${stats.stale ? 'offline' : ''}`} />
      <span data-testid="hud-online-count">{state.online} / 200</span>
      <span data-testid="hud-ping" className={delayed ? 'connection-warn' : ''} title="Round-trip network latency">{ping === null ? '—' : ping} ms</span>
      <span data-testid="hud-fps" title="Frames per second">{stats.fps ?? '—'} FPS</span>
    </div>
    {stats.stale ? <span role="status" className="connection-warn" data-testid="hud-stale-connection">WAITING FOR CONNECTION</span> : <span className="connection-detail" data-testid="hud-network-details" title="Latency jitter / server tick duration">±{Math.round(state.network?.jitter || 0)} ms · SV {Math.round(state.tick_ms || 0)} ms</span>}
  </div>;
};