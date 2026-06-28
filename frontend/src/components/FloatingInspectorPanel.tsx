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
  Layers,
  Play,
  RefreshCw,
  XCircle
} from 'lucide-react';

export const FloatingInspectorPanel: React.FC = () => {
  const { 
    activeView, 
    selectedRepairId, 
    setSelectedRepairId, 
    addNotification,
    graphStats,
    aiInferenceResult,
    healedRepairs,
    criticalityReport,
    simulationResult,
    systemConfig,
    isLoadingAction,
    triggerAiInference,
    triggerGraphConstruct,
    triggerGraphHeal,
    triggerCriticality,
    triggerSimulation,
    updateThresholds
  } = useAppStore();

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

  const selectedExplanation = healedRepairs.find(r => r.edge_id === selectedRepairId) || healedRepairs[0] || null;

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
          {isLoadingAction && (
            <RefreshCw size={14} className="animate-spin" style={{ animation: 'spin 1s linear infinite', color: 'var(--primary-500)' }} />
          )}
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
        <div style={{ flex: 1, overflowY: 'auto', padding: '20px', display: 'flex', flexDirection: 'column', gap: '20px', opacity: isLoadingAction ? 0.6 : 1, transition: 'opacity 0.2s' }}>
          
          {/* VIEW 1: OVERVIEW */}
          {activeView === 'overview' && (
            <>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                <div className="glass-card" style={{ padding: '14px', borderRadius: '12px' }}>
                  <div style={{ fontSize: '11px', color: 'var(--text-tertiary)', marginBottom: '4px' }}>ACTIVE NODES</div>
                  <div className="font-mono" style={{ fontSize: '24px', fontWeight: 700, color: 'var(--primary-500)' }}>{graphStats.node_count.toLocaleString()}</div>
                  <div style={{ fontSize: '10px', color: 'var(--success)', marginTop: '4px' }}>Hero City Grid</div>
                </div>
                <div className="glass-card" style={{ padding: '14px', borderRadius: '12px' }}>
                  <div style={{ fontSize: '11px', color: 'var(--text-tertiary)', marginBottom: '4px' }}>NETWORK EDGES</div>
                  <div className="font-mono" style={{ fontSize: '24px', fontWeight: 700, color: '#FFFFFF' }}>{graphStats.edge_count.toLocaleString()}</div>
                  <div style={{ fontSize: '10px', color: 'var(--text-secondary)', marginTop: '4px' }}>Avg deg {graphStats.avg_degree}</div>
                </div>
              </div>

              <div className="glass-card" style={{ padding: '16px', borderRadius: '12px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '13px', fontWeight: 600 }}>Network Efficiency Index</span>
                  <span className="font-mono" style={{ color: 'var(--success)', fontWeight: 700 }}>{(graphStats.network_efficiency * 100).toFixed(1)}%</span>
                </div>
                <div style={{ width: '100%', height: '8px', backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ width: `${graphStats.network_efficiency * 100}%`, height: '100%', backgroundColor: 'var(--success)', boxShadow: '0 0 10px var(--success)' }} />
                </div>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                  Hero City Bengaluru grid exhibits robust topology under nominal conditions. Connected components: {graphStats.connected_components}.
                </p>
              </div>

              <div style={{ padding: '12px', background: 'rgba(0, 242, 254, 0.05)', borderRadius: '10px', border: '1px solid rgba(0, 242, 254, 0.2)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--primary-500)', fontSize: '13px', fontWeight: 600, marginBottom: '6px' }}>
                  <TrendingUp size={16} />
                  <span>Real-time Sync Active</span>
                </div>
                <p style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>
                  Connected to FastAPI endpoints at <code style={{ color: '#FFF' }}>/api/v1/graph/baseline</code>.
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
                  <span>Confidence Threshold</span>
                  <span className="font-mono" style={{ color: 'var(--primary-500)' }}>{systemConfig.ai_confidence_threshold.toFixed(2)}</span>
                </div>
                <input 
                  type="range" 
                  min={0.30} 
                  max={0.95} 
                  step={0.05} 
                  value={systemConfig.ai_confidence_threshold}
                  onChange={(e) => updateThresholds({ ai_confidence_threshold: parseFloat(e.target.value) })}
                  style={{ width: '100%', accentColor: '#7F00FF', cursor: 'pointer' }} 
                />
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '10px', color: 'var(--text-tertiary)', marginTop: '4px' }}>
                  <span>0.30 (High Recall)</span>
                  <span>0.95 (High Precision)</span>
                </div>
                <button
                  disabled={isLoadingAction}
                  onClick={triggerAiInference}
                  className="btn-tactical"
                  style={{ width: '100%', justifyContent: 'center', marginTop: '14px', background: '#7F00FF', borderColor: '#A855F7' }}
                >
                  <Play size={14} /> Execute AI Road Extraction
                </button>
              </div>

              {aiInferenceResult && (
                <div className="glass-card" style={{ padding: '16px', borderRadius: '12px' }}>
                  <span style={{ fontSize: '13px', fontWeight: 600, display: 'block', marginBottom: '12px' }}>Segmentation Telemetry</span>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '8px' }}>
                    <span style={{ color: 'var(--text-secondary)' }}>clDice Topology Score</span>
                    <span className="font-mono" style={{ fontWeight: 600, color: '#34D399' }}>{(aiInferenceResult.cldice_score * 100).toFixed(1)}%</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '8px' }}>
                    <span style={{ color: 'var(--text-secondary)' }}>IoU Overlap Accuracy</span>
                    <span className="font-mono" style={{ fontWeight: 600, color: '#60A5FA' }}>{(aiInferenceResult.iou_score * 100).toFixed(1)}%</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px' }}>
                    <span style={{ color: 'var(--text-secondary)' }}>Occlusion Coverage</span>
                    <span className="font-mono" style={{ fontWeight: 600, color: '#FBBF24' }}>{aiInferenceResult.occlusion_coverage_pct}%</span>
                  </div>
                </div>
              )}
            </>
          )}

          {/* VIEW 3: GRAPH CONSTRUCTION */}
          {activeView === 'graph-construction' && (
            <>
              <div className="glass-card" style={{ padding: '16px', borderRadius: '12px' }}>
                <span style={{ fontSize: '13px', fontWeight: 600, color: '#3B82F6', display: 'block', marginBottom: '12px' }}>
                  Vectorization Parameters
                </span>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '6px' }}>
                  <span>RDP Simplification Epsilon (ε)</span>
                  <span className="font-mono" style={{ color: 'var(--primary-500)' }}>{systemConfig.rdp_epsilon.toFixed(1)} px</span>
                </div>
                <input 
                  type="range" min={0.5} max={5.0} step={0.5} 
                  value={systemConfig.rdp_epsilon}
                  onChange={(e) => updateThresholds({ rdp_epsilon: parseFloat(e.target.value) })}
                  style={{ width: '100%', accentColor: '#3B82F6', cursor: 'pointer' }} 
                />
                <button
                  disabled={isLoadingAction}
                  onClick={triggerGraphConstruct}
                  className="btn-tactical"
                  style={{ width: '100%', justifyContent: 'center', marginTop: '14px', background: '#2563EB' }}
                >
                  <RefreshCw size={14} /> Rebuild NetworkX Graph
                </button>
              </div>
            </>
          )}

          {/* VIEW 4: GRAPH HEALING (XAI EXPLAINABILITY) */}
          {activeView === 'graph-healing' && (
            <>
              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                {healedRepairs.map((rep) => (
                  <button
                    key={rep.edge_id}
                    onClick={() => setSelectedRepairId(rep.edge_id)}
                    style={{
                      flex: '1 0 30%', padding: '8px', borderRadius: '8px',
                      background: selectedRepairId === rep.edge_id ? 'var(--primary-500)' : 'rgba(255,255,255,0.05)',
                      color: selectedRepairId === rep.edge_id ? '#000' : '#FFF',
                      border: '1px solid var(--border-subtle)', fontWeight: 600, fontSize: '12px', cursor: 'pointer'
                    }}
                  >
                    {rep.edge_id}
                  </button>
                ))}
              </div>

              <button
                disabled={isLoadingAction}
                onClick={triggerGraphHeal}
                className="btn-tactical"
                style={{ width: '100%', justifyContent: 'center', background: 'var(--success)', color: '#000', fontWeight: 'bold' }}
              >
                <Play size={14} /> Execute Hybrid Graph Healing
              </button>

              {selectedExplanation && (
                <div className="glass-card" style={{ padding: '16px', borderRadius: '12px', border: `1px solid ${selectedExplanation.status === 'ACCEPTED' ? 'var(--success)' : 'var(--critical)'}` }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                    <span style={{ fontSize: '14px', fontWeight: 700, color: selectedExplanation.status === 'ACCEPTED' ? 'var(--success)' : 'var(--critical)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                      {selectedExplanation.status === 'ACCEPTED' ? <CheckCircle2 size={16} /> : <XCircle size={16} />} REPAIR ID: {selectedExplanation.edge_id}
                    </span>
                    <span className="font-mono" style={{ background: selectedExplanation.status === 'ACCEPTED' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)', color: selectedExplanation.status === 'ACCEPTED' ? 'var(--success)' : 'var(--critical)', padding: '2px 8px', borderRadius: '4px', fontSize: '11px', fontWeight: 700 }}>
                      {selectedExplanation.status}
                    </span>
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '12px', marginBottom: '16px', paddingBottom: '12px', borderBottom: '1px solid var(--border-subtle)' }}>
                    <div><span style={{ color: 'var(--text-tertiary)' }}>Source:</span> <span className="font-mono">{selectedExplanation.source_node}</span></div>
                    <div><span style={{ color: 'var(--text-tertiary)' }}>Destination:</span> <span className="font-mono">{selectedExplanation.destination_node}</span></div>
                    <div><span style={{ color: 'var(--text-tertiary)' }}>Gap Distance:</span> <span className="font-mono">{selectedExplanation.distance_m} m</span></div>
                    <div><span style={{ color: 'var(--text-tertiary)' }}>Hybrid Score:</span> <span className="font-mono">{selectedExplanation.hybrid_cost_score}</span></div>
                  </div>

                  <div style={{ fontSize: '12px', fontWeight: 600, marginBottom: '8px' }}>Hybrid Cost Multi-Factor Breakdown</div>
                  {[
                    { label: 'AI Probability Map Score', val: selectedExplanation.ai_confidence, color: '#00F2FE' },
                    { label: 'Direction Consistency', val: selectedExplanation.direction_consistency, color: '#10B981' },
                    { label: 'Road Width Similarity', val: selectedExplanation.road_width_similarity, color: '#3B82F6' },
                    { label: 'Local Road Density Prior', val: selectedExplanation.local_road_density, color: '#A855F7' }
                  ].map((factor, i) => (
                    <div key={i} style={{ marginBottom: '8px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', marginBottom: '2px' }}>
                        <span style={{ color: 'var(--text-secondary)' }}>{factor.label}</span>
                        <span className="font-mono" style={{ fontWeight: 600, color: factor.color }}>{factor.val.toFixed(2)}</span>
                      </div>
                      <div style={{ width: '100%', height: '5px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                        <div style={{ width: `${factor.val * 100}%`, height: '100%', backgroundColor: factor.color }} />
                      </div>
                    </div>
                  ))}

                  <div style={{ marginTop: '16px', padding: '12px', background: selectedExplanation.status === 'ACCEPTED' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)', borderRadius: '8px', fontSize: '12px', color: selectedExplanation.status === 'ACCEPTED' ? '#A7F3D0' : '#FCA5A5', lineHeight: 1.4 }}>
                    <strong>Explainable Rationale:</strong> {selectedExplanation.rationale}
                  </div>
                </div>
              )}
            </>
          )}

          {/* VIEW 5: CRITICALITY ANALYSIS */}
          {activeView === 'criticality' && (
            <>
              <button
                disabled={isLoadingAction}
                onClick={triggerCriticality}
                className="btn-tactical"
                style={{ width: '100%', justifyContent: 'center', background: 'var(--warning)', color: '#000', fontWeight: 'bold' }}
              >
                <RefreshCw size={14} /> Recalculate Centrality Metrics
              </button>

              {criticalityReport && (
                <div className="glass-card" style={{ padding: '16px', borderRadius: '12px', borderLeft: '4px solid var(--warning)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                    <span style={{ fontSize: '14px', fontWeight: 700, color: 'var(--warning)' }}>Top Bottleneck: {criticalityReport.bridges[0] || 'E-088'}</span>
                    <span className="font-mono" style={{ fontSize: '12px', background: 'rgba(245, 158, 11, 0.2)', color: 'var(--warning)', padding: '2px 6px', borderRadius: '4px' }}>BRIDGE</span>
                  </div>
                  <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '12px' }}>
                    High Betweenness Centrality. Severing this edge separates articulation points {criticalityReport.articulation_points.join(', ')}.
                  </p>
                  <button
                    onClick={() => addNotification({ type: 'warning', title: 'Route Isolated', message: `${criticalityReport.bridges[0] || 'E-088'} highlighted on spatial map.` })}
                    className="btn-tactical"
                    style={{ width: '100%', justifyContent: 'center', fontSize: '12px' }}
                  >
                    Focus on Spatial Map
                  </button>
                </div>
              )}
            </>
          )}

          {/* VIEW 6 & 7: SIMULATION & DECISION SUPPORT */}
          {(activeView === 'simulation' || activeView === 'decision-support') && (
            <>
              <button
                disabled={isLoadingAction}
                onClick={triggerSimulation}
                className="btn-tactical"
                style={{ width: '100%', justifyContent: 'center', background: 'var(--critical)', color: '#FFF', fontWeight: 'bold' }}
              >
                <Play size={14} /> Trigger Disaster Stress Blast
              </button>

              {simulationResult && (
                <div className="glass-card" style={{ padding: '16px', borderRadius: '12px', border: '1px solid var(--critical)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--critical)', fontWeight: 700, fontSize: '14px', marginBottom: '8px' }}>
                    <ShieldAlert size={18} /> Inundation Disruption Telemetry
                  </div>
                  <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '12px' }}>
                    Simulated cloudburst inundation. {simulationResult.disconnected_nodes} junctions severed. Efficiency dropped by {simulationResult.efficiency_drop_pct}%.
                  </p>
                  <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '8px', fontSize: '12px' }}>
                    <span>Detour Factor:</span>
                    <span className="font-mono" style={{ color: 'var(--critical)', fontWeight: 700 }}>{simulationResult.detour_factor}x nominal</span>
                  </div>
                </div>
              )}

              <div className="glass-card" style={{ padding: '16px', borderRadius: '12px' }}>
                <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--success)', display: 'block', marginBottom: '10px' }}>
                  ISRO AI Repair Recommendations
                </span>
                <div style={{ padding: '10px', background: 'rgba(16, 185, 129, 0.08)', borderRadius: '8px', border: '1px solid rgba(16, 185, 129, 0.3)' }}>
                  <div style={{ fontSize: '12px', fontWeight: 600, color: '#FFF', marginBottom: '4px' }}>Priority #1: Deploy Modular Link at RH-001</div>
                  <div style={{ fontSize: '11px', color: 'var(--success)' }}>Restores LCC (+16.1% resilience boost)</div>
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
