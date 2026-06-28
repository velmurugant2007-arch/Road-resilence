import React, { useState } from 'react';
import { useAppStore } from '../store/useAppStore';
import { 
  Minimize2, 
  Maximize2, 
  Cpu, 
  Share2, 
  HeartHandshake, 
  AlertTriangle, 
  Activity, 
  CheckSquare, 
  Sliders, 
  CheckCircle2, 
  ShieldAlert,
  TrendingUp,
  Layers
} from 'lucide-react';

export const FloatingInspectorPanel: React.FC = () => {
  const { activeView, selectedRepairId, setSelectedRepairId, addNotification } = useAppStore();
  const [isMinimized, setIsMinimized] = useState(false);

  const getHeaderInfo = () => {
    switch (activeView) {
      case 'overview': return { title: 'System Telemetry & Grid Metrics', icon: <Layers size={18} color="var(--primary-500)" /> };
      case 'ai-extraction': return { title: 'AI Segmentation Shaders (SegFormer)', icon: <Cpu size={18} color="#7F00FF" /> };
      case 'graph-construction': return { title: 'Graph Vectorization & RDP Tuning', icon: <Share2 size={18} color="#3B82F6" /> };
      case 'graph-healing': return { title: 'XAI Explainable Repair Inspector', icon: <HeartHandshake size={18} color="var(--success)" /> };
      case 'criticality': return { title: 'Centrality & Bottleneck Ranking', icon: <AlertTriangle size={18} color="var(--warning)" /> };
      case 'simulation': return { title: 'Disaster Stress Simulation Matrix', icon: <Activity size={18} color="var(--critical)" /> };
      case 'decision-support': return { title: 'Decision Support & Repair Priority', icon: <CheckSquare size={18} color="var(--success)" /> };
      case 'config': return { title: 'ISRO System Configuration Parameters', icon: <Sliders size={18} color="var(--primary-500)" /> };
    }
  };

  const { title, icon } = getHeaderInfo();

  return (
    <div className="glass-panel" style={{
      position: 'fixed',
      top: '92px',
      right: '24px',
      bottom: '92px',
      width: '400px',
      borderRadius: '20px',
      display: 'flex',
      flexDirection: 'column',
      zIndex: 350,
      overflow: 'hidden',
      transition: 'height 0.2s ease',
      height: isMinimized ? '56px' : 'auto'
    }}>
      {/* Panel Header */}
      <div style={{
        padding: '16px 20px',
        borderBottom: '1px solid var(--border-subtle)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        backgroundColor: 'rgba(0,0,0,0.2)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {icon}
          <span style={{ fontSize: '15px', fontWeight: 600, fontFamily: "'Outfit', sans-serif" }}>{title}</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <button
            onClick={() => setIsMinimized(!isMinimized)}
            style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer' }}
          >
            {isMinimized ? <Maximize2 size={16} /> : <Minimize2 size={16} />}
          </button>
        </div>
      </div>

      {/* Panel Content Body */}
      {!isMinimized && (
        <div style={{ flex: 1, overflowY: 'auto', padding: '20px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* VIEW 1: OVERVIEW */}
          {activeView === 'overview' && (
            <>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                <div className="glass-card" style={{ padding: '14px', borderRadius: '12px' }}>
                  <div style={{ fontSize: '11px', color: 'var(--text-tertiary)', marginBottom: '4px' }}>ACTIVE NODES</div>
                  <div className="font-mono" style={{ fontSize: '24px', fontWeight: 700, color: 'var(--primary-500)' }}>1,240</div>
                  <div style={{ fontSize: '10px', color: 'var(--success)', marginTop: '4px' }}>+12% vs baseline</div>
                </div>
                <div className="glass-card" style={{ padding: '14px', borderRadius: '12px' }}>
                  <div style={{ fontSize: '11px', color: 'var(--text-tertiary)', marginBottom: '4px' }}>NETWORK EDGES</div>
                  <div className="font-mono" style={{ fontSize: '24px', fontWeight: 700, color: '#FFFFFF' }}>1,890</div>
                  <div style={{ fontSize: '10px', color: 'var(--text-secondary)', marginTop: '4px' }}>142.6 km total</div>
                </div>
              </div>

              <div className="glass-card" style={{ padding: '16px', borderRadius: '12px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '13px', fontWeight: 600 }}>Largest Connected Component (LCC)</span>
                  <span className="font-mono" style={{ color: 'var(--success)', fontWeight: 700 }}>99.4%</span>
                </div>
                <div style={{ width: '100%', height: '8px', backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ width: '99.4%', height: '100%', backgroundColor: 'var(--success)', boxShadow: '0 0 10px var(--success)' }} />
                </div>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                  Hero City Bengaluru grid exhibits robust topology under nominal conditions. Graph density is 0.0024 with average degree 3.04.
                </p>
              </div>

              <div style={{ padding: '12px', background: 'rgba(0, 242, 254, 0.05)', borderRadius: '10px', border: '1px solid rgba(0, 242, 254, 0.2)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--primary-500)', fontSize: '13px', fontWeight: 600, marginBottom: '6px' }}>
                  <TrendingUp size={16} />
                  <span>Real-time Sync Active</span>
                </div>
                <p style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>
                  Connected to FastAPI backend at <code style={{ color: '#FFF' }}>/api/v1/graph/stats</code>. Map cache TTL is set to 300 seconds.
                </p>
              </div>
            </>
          )}

          {/* VIEW 2: AI EXTRACTION */}
          {activeView === 'ai-extraction' && (
            <>
              <div className="glass-card" style={{ padding: '16px', borderRadius: '12px' }}>
                <span style={{ fontSize: '13px', fontWeight: 600, color: '#7F00FF', display: 'block', marginBottom: '12px' }}>
                  SegFormer MiT-B2 Inference Controls
                </span>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '6px' }}>
                  <span>Probability Mask Threshold</span>
                  <span className="font-mono" style={{ color: 'var(--primary-500)' }}>0.85</span>
                </div>
                <input type="range" min={0.5} max={0.99} step={0.01} defaultValue={0.85} style={{ width: '100%', accentColor: '#7F00FF' }} />
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '10px', color: 'var(--text-tertiary)', marginTop: '4px' }}>
                  <span>0.50 (High Recall)</span>
                  <span>0.99 (High Precision)</span>
                </div>
              </div>

              <div className="glass-card" style={{ padding: '16px', borderRadius: '12px' }}>
                <span style={{ fontSize: '13px', fontWeight: 600, display: 'block', marginBottom: '12px' }}>Occlusion Classification</span>
                {[
                  { label: 'Cloud Cover & Shadow', pct: '42%', color: '#60A5FA' },
                  { label: 'Tree Canopy Overhang', pct: '38%', color: '#34D399' },
                  { label: 'Building Shadow Artifacts', pct: '20%', color: '#FBBF24' }
                ].map((occ, i) => (
                  <div key={i} style={{ marginBottom: '10px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                      <span style={{ color: 'var(--text-secondary)' }}>{occ.label}</span>
                      <span className="font-mono" style={{ fontWeight: 600 }}>{occ.pct}</span>
                    </div>
                    <div style={{ width: '100%', height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                      <div style={{ width: occ.pct, height: '100%', backgroundColor: occ.color }} />
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}

          {/* VIEW 4: GRAPH HEALING (XAI EXPLAINABILITY) */}
          {activeView === 'graph-healing' && (
            <>
              <div style={{ display: 'flex', gap: '8px' }}>
                {['RH-001', 'RH-002', 'RH-003'].map((id) => (
                  <button
                    key={id}
                    onClick={() => setSelectedRepairId(id)}
                    style={{
                      flex: 1, padding: '8px', borderRadius: '8px',
                      background: selectedRepairId === id || (!selectedRepairId && id === 'RH-001') ? 'var(--primary-500)' : 'rgba(255,255,255,0.05)',
                      color: selectedRepairId === id || (!selectedRepairId && id === 'RH-001') ? '#000' : '#FFF',
                      border: '1px solid var(--border-subtle)', fontWeight: 600, fontSize: '12px', cursor: 'pointer'
                    }}
                  >
                    {id}
                  </button>
                ))}
              </div>

              <div className="glass-card" style={{ padding: '16px', borderRadius: '12px', border: '1px solid var(--success)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                  <span style={{ fontSize: '14px', fontWeight: 700, color: 'var(--success)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <CheckCircle2 size={16} /> REPAIR ID: {selectedRepairId || 'RH-001'}
                  </span>
                  <span className="font-mono" style={{ background: 'rgba(16, 185, 129, 0.2)', color: 'var(--success)', padding: '2px 8px', borderRadius: '4px', fontSize: '11px', fontWeight: 700 }}>
                    ACCEPTED
                  </span>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '12px', marginBottom: '16px', paddingBottom: '12px', borderBottom: '1px solid var(--border-subtle)' }}>
                  <div><span style={{ color: 'var(--text-tertiary)' }}>Source:</span> <span className="font-mono">N154</span></div>
                  <div><span style={{ color: 'var(--text-tertiary)' }}>Destination:</span> <span className="font-mono">N173</span></div>
                  <div><span style={{ color: 'var(--text-tertiary)' }}>Gap Distance:</span> <span className="font-mono">8.2 m</span></div>
                  <div><span style={{ color: 'var(--text-tertiary)' }}>Threshold:</span> <span className="font-mono">0.75</span></div>
                </div>

                <div style={{ fontSize: '12px', fontWeight: 600, marginBottom: '8px' }}>Hybrid Cost Multi-Factor Breakdown</div>
                {[
                  { label: 'AI Probability Map Score', val: 0.91, color: '#00F2FE' },
                  { label: 'Direction Consistency', val: 0.96, color: '#10B981' },
                  { label: 'Road Width Similarity', val: 0.88, color: '#3B82F6' },
                  { label: 'Local Road Density Prior', val: 0.84, color: '#A855F7' }
                ].map((factor, i) => (
                  <div key={i} style={{ marginBottom: '8px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', marginBottom: '2px' }}>
                      <span style={{ color: 'var(--text-secondary)' }}>{factor.label}</span>
                      <span className="font-mono" style={{ fontWeight: 600, color: factor.color }}>{factor.val}</span>
                    </div>
                    <div style={{ width: '100%', height: '5px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                      <div style={{ width: `${factor.val * 100}%`, height: '100%', backgroundColor: factor.color }} />
                    </div>
                  </div>
                ))}

                <div style={{ marginTop: '16px', padding: '12px', background: 'rgba(16, 185, 129, 0.1)', borderRadius: '8px', fontSize: '12px', color: '#A7F3D0', lineHeight: 1.4 }}>
                  <strong>Explainable Decision:</strong> Accepted because the hybrid score (0.93) exceeded threshold (0.75), directional angle deviation is &lt;5°, and no physical barrier (water/rail) vetoed the connection.
                </div>
              </div>
            </>
          )}

          {/* VIEW 5: CRITICALITY ANALYSIS */}
          {activeView === 'criticality' && (
            <>
              <div className="glass-card" style={{ padding: '16px', borderRadius: '12px', borderLeft: '4px solid var(--warning)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <span style={{ fontSize: '14px', fontWeight: 700, color: 'var(--warning)' }}>Top Bottleneck: Silk Board Flyover</span>
                  <span className="font-mono" style={{ fontSize: '12px', background: 'rgba(245, 158, 11, 0.2)', color: 'var(--warning)', padding: '2px 6px', borderRadius: '4px' }}>E-088</span>
                </div>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '12px' }}>
                  High Betweenness Centrality (0.94). Severing this edge isolates 42% of south-eastern connectivity during flood events.
                </p>
                <button
                  onClick={() => addNotification({ type: 'warning', title: 'Route Isolated', message: 'E-088 highlighted on spatial canvas.' })}
                  className="btn-tactical"
                  style={{ width: '100%', justifyContent: 'center', fontSize: '12px' }}
                >
                  Focus on Spatial Map
                </button>
              </div>
            </>
          )}

          {/* VIEW 6 & 7: SIMULATION & DECISION SUPPORT */}
          {(activeView === 'simulation' || activeView === 'decision-support') && (
            <>
              <div className="glass-card" style={{ padding: '16px', borderRadius: '12px', border: '1px solid var(--critical)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--critical)', fontWeight: 700, fontSize: '14px', marginBottom: '8px' }}>
                  <ShieldAlert size={18} /> Indiranagar Corridor Flood Failure
                </div>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '12px' }}>
                  Simulated 500mm cloudburst inundation. 14 critical junction nodes submerged. Network connectivity dropped from 99.4% to 78.1%.
                </p>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '8px', fontSize: '12px' }}>
                  <span>Est. Travel Delay:</span>
                  <span className="font-mono" style={{ color: 'var(--critical)', fontWeight: 700 }}>+44 mins</span>
                </div>
              </div>

              <div className="glass-card" style={{ padding: '16px', borderRadius: '12px' }}>
                <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--success)', display: 'block', marginBottom: '10px' }}>
                  ISRO AI Repair Recommendations
                </span>
                <div style={{ padding: '10px', background: 'rgba(16, 185, 129, 0.08)', borderRadius: '8px', border: '1px solid rgba(16, 185, 129, 0.3)' }}>
                  <div style={{ fontSize: '12px', fontWeight: 600, color: '#FFF', marginBottom: '4px' }}>Priority #1: Deploy Modular Pontoon at E-088</div>
                  <div style={{ fontSize: '11px', color: 'var(--success)' }}>Restores LCC to 94.2% (+16.1% resilience boost)</div>
                </div>
              </div>
            </>
          )}

          {/* VIEW 8: CONFIG */}
          {activeView === 'config' && (
            <div className="glass-card" style={{ padding: '16px', borderRadius: '12px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div>
                <label style={{ fontSize: '12px', color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>FastAPI Backend Endpoint</label>
                <input type="text" readOnly defaultValue="http://127.0.0.1:8000/api/v1" className="font-mono" style={{ width: '100%', padding: '8px', background: 'rgba(0,0,0,0.4)', border: '1px solid var(--border-subtle)', borderRadius: '6px', color: '#FFF', fontSize: '12px' }} />
              </div>
              <button
                onClick={() => addNotification({ type: 'success', title: 'Cache Purged', message: 'Hero City spatial grid cache cleared.' })}
                className="btn-tactical"
                style={{ justifyContent: 'center' }}
              >
                Purge Spatial Grid Cache
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
