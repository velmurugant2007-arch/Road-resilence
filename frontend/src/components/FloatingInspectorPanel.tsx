import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAppStore } from '../store/useAppStore';
import { 
  Minimize2, Maximize2, Cpu, Share2, HeartHandshake, AlertTriangle, 
  Activity, CheckSquare, Sliders, CheckCircle2, ShieldAlert, TrendingUp,
  Layers, Play, RefreshCw, XCircle, Zap, Target, ArrowRight
} from 'lucide-react';

/* ─── Reusable Empty State ─── */
const EmptyState: React.FC<{ icon: React.ReactNode; title: string; description: string; action?: { label: string; onClick: () => void } }> = ({ icon, title, description, action }) => (
  <div className="empty-state animate-fade-in">
    <div className="empty-state-icon">{icon}</div>
    <div className="empty-state-title">{title}</div>
    <div className="empty-state-desc">{description}</div>
    {action && (
      <button onClick={action.onClick} className="btn-tactical" style={{ marginTop: '4px', fontSize: '12px' }}>
        {action.label} <ArrowRight size={12} />
      </button>
    )}
  </div>
);

/* ─── Metric Row ─── */
const MetricRow: React.FC<{ label: string; value: string; color?: string }> = ({ label, value, color }) => (
  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '12px', padding: '6px 0' }}>
    <span style={{ color: 'var(--text-secondary)' }}>{label}</span>
    <span className="font-mono" style={{ fontWeight: 600, color: color || 'var(--text-primary)' }}>{value}</span>
  </div>
);

/* ─── Progress Bar ─── */
const Bar: React.FC<{ label: string; value: number; color: string }> = ({ label, value, color }) => (
  <div style={{ marginBottom: '10px' }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', marginBottom: '3px' }}>
      <span style={{ color: 'var(--text-secondary)' }}>{label}</span>
      <span className="font-mono" style={{ fontWeight: 600, color }}>{value.toFixed(2)}</span>
    </div>
    <div className="progress-track">
      <div className="progress-fill" style={{ width: `${value * 100}%`, backgroundColor: color, boxShadow: `0 0 8px ${color}40` }} />
    </div>
  </div>
);

export const FloatingInspectorPanel: React.FC = () => {
  const { 
    activeView, selectedRepairId, setSelectedRepairId, addNotification,
    graphStats, aiInferenceResult, healedRepairs, criticalityReport,
    simulationResult, systemConfig, isLoadingAction, backendHealth,
    triggerAiInference, triggerGraphConstruct, triggerGraphHeal,
    triggerCriticality, triggerSimulation, updateThresholds, initBackendSync
  } = useAppStore();

  const [isMinimized, setIsMinimized] = useState(false);

  const headers: Record<string, { title: string; icon: React.ReactNode }> = {
    'overview': { title: 'System Telemetry', icon: <Layers size={16} color="var(--primary-500)" /> },
    'ai-extraction': { title: 'AI Segmentation', icon: <Cpu size={16} color="#7F00FF" /> },
    'graph-construction': { title: 'Graph Vectorization', icon: <Share2 size={16} color="#3B82F6" /> },
    'graph-healing': { title: 'XAI Repair Inspector', icon: <HeartHandshake size={16} color="var(--success)" /> },
    'criticality': { title: 'Criticality Ranking', icon: <AlertTriangle size={16} color="var(--warning)" /> },
    'simulation': { title: 'Stress Simulation', icon: <Activity size={16} color="var(--critical)" /> },
    'decision-support': { title: 'Decision Support', icon: <CheckSquare size={16} color="var(--success)" /> },
    'config': { title: 'Configuration', icon: <Sliders size={16} color="var(--primary-500)" /> },
  };

  const { title, icon } = headers[activeView] || headers.overview;
  const selectedExplanation = healedRepairs.find(r => r.edge_id === selectedRepairId) || healedRepairs[0] || null;

  const panelVariants = {
    hidden: { opacity: 0, y: 8 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.2, ease: [0.22, 1, 0.36, 1] as const } },
    exit: { opacity: 0, y: -4, transition: { duration: 0.12 } },
  };

  return (
    <div className="glass-panel" style={{
      position: 'fixed', top: '88px', right: 'var(--sp-6)', bottom: '88px',
      width: '392px', borderRadius: 'var(--radius-xl)',
      display: 'flex', flexDirection: 'column', zIndex: 350, overflow: 'hidden',
    }}>
      {/* Header */}
      <div style={{
        padding: '14px var(--sp-5)', borderBottom: '1px solid var(--border-subtle)',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        background: 'rgba(0,0,0,0.15)', flexShrink: 0,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--sp-2)' }}>
          {icon}
          <span style={{ fontSize: '13px', fontWeight: 600, fontFamily: "'Outfit', sans-serif", color: 'var(--text-primary)' }}>{title}</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          {isLoadingAction && (
            <RefreshCw size={13} style={{ animation: 'spin 1s linear infinite', color: 'var(--primary-500)' }} />
          )}
          <button
            onClick={() => setIsMinimized(!isMinimized)}
            className="icon-btn"
            style={{ width: '26px', height: '26px', border: 'none' }}
          >
            {isMinimized ? <Maximize2 size={13} /> : <Minimize2 size={13} />}
          </button>
        </div>
      </div>

      {/* Body */}
      {!isMinimized && (
        <div style={{
          flex: 1, overflowY: 'auto', padding: 'var(--sp-4) var(--sp-5)',
          display: 'flex', flexDirection: 'column', gap: 'var(--sp-4)',
          opacity: isLoadingAction ? 0.55 : 1, transition: 'opacity 0.2s',
          pointerEvents: isLoadingAction ? 'none' : 'auto',
        }}>
          <AnimatePresence mode="wait">
            <motion.div key={activeView} variants={panelVariants} initial="hidden" animate="visible" exit="exit"
              style={{ display: 'flex', flexDirection: 'column', gap: 'var(--sp-4)' }}>

              {/* ── OVERVIEW ── */}
              {activeView === 'overview' && (
                <>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--sp-3)' }}>
                    <div className="glass-card metric-card">
                      <div className="metric-label">Active Nodes</div>
                      <div className="metric-value font-mono" style={{ color: 'var(--primary-500)' }}>{graphStats.node_count.toLocaleString()}</div>
                      <div className="metric-sub" style={{ color: 'var(--success)' }}>Hero City Grid</div>
                    </div>
                    <div className="glass-card metric-card">
                      <div className="metric-label">Network Edges</div>
                      <div className="metric-value font-mono">{graphStats.edge_count.toLocaleString()}</div>
                      <div className="metric-sub" style={{ color: 'var(--text-tertiary)' }}>Avg deg {graphStats.avg_degree}</div>
                    </div>
                  </div>

                  <div className="glass-card" style={{ padding: 'var(--sp-4)', borderRadius: 'var(--radius-md)' }}>
                    <MetricRow label="Network Efficiency" value={`${(graphStats.network_efficiency * 100).toFixed(1)}%`} color="var(--success)" />
                    <div className="progress-track" style={{ marginTop: '6px' }}>
                      <div className="progress-fill" style={{ width: `${graphStats.network_efficiency * 100}%`, backgroundColor: 'var(--success)', boxShadow: '0 0 10px rgba(16,185,129,0.4)' }} />
                    </div>
                    <MetricRow label="Connected Components" value={String(graphStats.connected_components)} />
                  </div>

                  <div style={{ padding: 'var(--sp-3)', background: 'rgba(0, 242, 254, 0.04)', borderRadius: 'var(--radius-md)', border: '1px solid rgba(0, 242, 254, 0.12)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--primary-500)', fontSize: '11px', fontWeight: 600 }}>
                      <TrendingUp size={13} />
                      <span>{backendHealth === 'healthy' ? 'Live Backend Sync' : 'Offline Cache Active'}</span>
                    </div>
                  </div>
                </>
              )}

              {/* ── AI EXTRACTION ── */}
              {activeView === 'ai-extraction' && (
                <>
                  <div className="glass-card" style={{ padding: 'var(--sp-4)', borderRadius: 'var(--radius-md)' }}>
                    <div className="section-header" style={{ color: '#7F00FF' }}>
                      <Zap size={14} /> Inference Controls
                    </div>
                    <MetricRow label="Confidence Threshold" value={systemConfig.ai_confidence_threshold.toFixed(2)} color="var(--primary-500)" />
                    <input 
                      type="range" min={0.30} max={0.95} step={0.05} 
                      value={systemConfig.ai_confidence_threshold}
                      onChange={(e) => updateThresholds({ ai_confidence_threshold: parseFloat(e.target.value) })}
                      style={{ width: '100%', accentColor: '#7F00FF', cursor: 'pointer', margin: '4px 0 8px' }} 
                    />
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '9px', color: 'var(--text-disabled)' }}>
                      <span>0.30 Recall</span><span>0.95 Precision</span>
                    </div>
                    <button
                      disabled={isLoadingAction}
                      onClick={triggerAiInference}
                      className="btn-tactical"
                      style={{ width: '100%', justifyContent: 'center', marginTop: 'var(--sp-4)', background: 'rgba(127, 0, 255, 0.3)', borderColor: '#A855F7' }}
                    >
                      <Play size={13} /> {isLoadingAction ? 'Processing...' : 'Execute AI Extraction'}
                    </button>
                  </div>

                  {aiInferenceResult ? (
                    <div className="glass-card" style={{ padding: 'var(--sp-4)', borderRadius: 'var(--radius-md)' }}>
                      <div className="section-header">Segmentation Telemetry</div>
                      <MetricRow label="clDice Topology" value={`${(aiInferenceResult.cldice_score * 100).toFixed(1)}%`} color="#34D399" />
                      <MetricRow label="IoU Overlap" value={`${(aiInferenceResult.iou_score * 100).toFixed(1)}%`} color="#60A5FA" />
                      <MetricRow label="Occlusion Coverage" value={`${aiInferenceResult.occlusion_coverage_pct}%`} color="#FBBF24" />
                    </div>
                  ) : (
                    <EmptyState 
                      icon={<Cpu size={20} />} 
                      title="No Inference Results" 
                      description="Run AI road extraction to generate segmentation metrics and probability maps."
                      action={{ label: 'Run Extraction', onClick: triggerAiInference }}
                    />
                  )}
                </>
              )}

              {/* ── GRAPH CONSTRUCTION ── */}
              {activeView === 'graph-construction' && (
                <>
                  <div className="glass-card" style={{ padding: 'var(--sp-4)', borderRadius: 'var(--radius-md)' }}>
                    <div className="section-header" style={{ color: '#3B82F6' }}>
                      <Target size={14} /> Vectorization Parameters
                    </div>
                    <MetricRow label="RDP Epsilon (ε)" value={`${systemConfig.rdp_epsilon.toFixed(1)} px`} color="var(--primary-500)" />
                    <input 
                      type="range" min={0.5} max={5.0} step={0.5} 
                      value={systemConfig.rdp_epsilon}
                      onChange={(e) => updateThresholds({ rdp_epsilon: parseFloat(e.target.value) })}
                      style={{ width: '100%', accentColor: '#3B82F6', cursor: 'pointer', margin: '4px 0 8px' }} 
                    />
                    <button
                      disabled={isLoadingAction}
                      onClick={triggerGraphConstruct}
                      className="btn-tactical"
                      style={{ width: '100%', justifyContent: 'center', marginTop: 'var(--sp-4)', background: 'rgba(37, 99, 235, 0.3)' }}
                    >
                      <RefreshCw size={13} /> {isLoadingAction ? 'Building...' : 'Rebuild NetworkX Graph'}
                    </button>
                  </div>

                  <div className="glass-card" style={{ padding: 'var(--sp-4)', borderRadius: 'var(--radius-md)' }}>
                    <div className="section-header">Current Topology</div>
                    <MetricRow label="Nodes" value={graphStats.node_count.toLocaleString()} color="var(--primary-500)" />
                    <MetricRow label="Edges" value={graphStats.edge_count.toLocaleString()} />
                    <MetricRow label="Components" value={String(graphStats.connected_components)} />
                    <MetricRow label="Avg Degree" value={String(graphStats.avg_degree)} color="#60A5FA" />
                  </div>
                </>
              )}

              {/* ── GRAPH HEALING ── */}
              {activeView === 'graph-healing' && (
                <>
                  <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                    {healedRepairs.map((rep) => (
                      <button
                        key={rep.edge_id}
                        onClick={() => setSelectedRepairId(rep.edge_id)}
                        style={{
                          flex: '1 0 28%', padding: '7px', borderRadius: 'var(--radius-sm)',
                          background: selectedRepairId === rep.edge_id ? 'var(--primary-500)' : 'rgba(255,255,255,0.04)',
                          color: selectedRepairId === rep.edge_id ? '#000' : 'var(--text-secondary)',
                          border: `1px solid ${selectedRepairId === rep.edge_id ? 'var(--primary-500)' : 'var(--border-subtle)'}`,
                          fontWeight: 600, fontSize: '11px', cursor: 'pointer',
                          transition: 'all var(--duration-fast) var(--ease-out)',
                        }}
                      >
                        {rep.edge_id}
                        <span style={{ display: 'block', fontSize: '9px', opacity: 0.7, marginTop: '1px' }}>
                          {rep.status === 'ACCEPTED' ? '✓' : '✗'} {rep.hybrid_cost_score.toFixed(2)}
                        </span>
                      </button>
                    ))}
                  </div>

                  <button
                    disabled={isLoadingAction}
                    onClick={triggerGraphHeal}
                    className="btn-tactical"
                    style={{ width: '100%', justifyContent: 'center', background: 'rgba(16,185,129,0.25)', borderColor: 'var(--success)', color: 'var(--success)' }}
                  >
                    <Play size={13} /> {isLoadingAction ? 'Healing...' : 'Execute Hybrid Healing'}
                  </button>

                  {selectedExplanation ? (
                    <div className="glass-card" style={{ padding: 'var(--sp-4)', borderRadius: 'var(--radius-md)', borderLeft: `3px solid ${selectedExplanation.status === 'ACCEPTED' ? 'var(--success)' : 'var(--critical)'}` }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--sp-3)' }}>
                        <span style={{ fontSize: '13px', fontWeight: 700, color: selectedExplanation.status === 'ACCEPTED' ? 'var(--success)' : 'var(--critical)', display: 'flex', alignItems: 'center', gap: '5px' }}>
                          {selectedExplanation.status === 'ACCEPTED' ? <CheckCircle2 size={14} /> : <XCircle size={14} />}
                          {selectedExplanation.edge_id}
                        </span>
                        <span className="font-mono" style={{ background: selectedExplanation.status === 'ACCEPTED' ? 'rgba(16,185,129,0.15)' : 'rgba(239,68,68,0.15)', color: selectedExplanation.status === 'ACCEPTED' ? 'var(--success)' : 'var(--critical)', padding: '2px 6px', borderRadius: '3px', fontSize: '10px', fontWeight: 700 }}>
                          {selectedExplanation.status}
                        </span>
                      </div>

                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4px 12px', fontSize: '11px', paddingBottom: 'var(--sp-3)', marginBottom: 'var(--sp-3)', borderBottom: '1px solid var(--border-subtle)' }}>
                        <MetricRow label="Source" value={selectedExplanation.source_node} />
                        <MetricRow label="Dest" value={selectedExplanation.destination_node} />
                        <MetricRow label="Gap" value={`${selectedExplanation.distance_m}m`} />
                        <MetricRow label="Score" value={selectedExplanation.hybrid_cost_score.toFixed(2)} color="var(--primary-500)" />
                      </div>

                      <Bar label="AI Confidence" value={selectedExplanation.ai_confidence} color="#00F2FE" />
                      <Bar label="Direction Consistency" value={selectedExplanation.direction_consistency} color="#10B981" />
                      <Bar label="Road Width Similarity" value={selectedExplanation.road_width_similarity} color="#3B82F6" />
                      <Bar label="Local Road Density" value={selectedExplanation.local_road_density} color="#A855F7" />

                      <div style={{ marginTop: 'var(--sp-3)', padding: 'var(--sp-3)', background: selectedExplanation.status === 'ACCEPTED' ? 'rgba(16,185,129,0.08)' : 'rgba(239,68,68,0.08)', borderRadius: 'var(--radius-sm)', fontSize: '11px', color: selectedExplanation.status === 'ACCEPTED' ? '#A7F3D0' : '#FCA5A5', lineHeight: 1.5 }}>
                        <strong>Rationale:</strong> {selectedExplanation.rationale}
                      </div>
                    </div>
                  ) : (
                    <EmptyState
                      icon={<HeartHandshake size={20} />}
                      title="No Repair Candidates"
                      description="Run graph healing to evaluate and repair fragmented road connections using the hybrid cost function."
                      action={{ label: 'Execute Healing', onClick: triggerGraphHeal }}
                    />
                  )}
                </>
              )}

              {/* ── CRITICALITY ── */}
              {activeView === 'criticality' && (
                <>
                  <button
                    disabled={isLoadingAction}
                    onClick={triggerCriticality}
                    className="btn-tactical"
                    style={{ width: '100%', justifyContent: 'center', background: 'rgba(245,158,11,0.2)', borderColor: 'var(--warning)', color: 'var(--warning)' }}
                  >
                    <RefreshCw size={13} /> {isLoadingAction ? 'Computing...' : 'Recalculate Centrality'}
                  </button>

                  {criticalityReport ? (
                    <>
                      <div className="glass-card" style={{ padding: 'var(--sp-4)', borderRadius: 'var(--radius-md)', borderLeft: '3px solid var(--warning)' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                          <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--warning)' }}>Top Bridge: {criticalityReport.bridges[0] || 'E-088'}</span>
                          <span className="font-mono" style={{ fontSize: '10px', background: 'rgba(245,158,11,0.15)', color: 'var(--warning)', padding: '2px 6px', borderRadius: '3px' }}>BRIDGE</span>
                        </div>
                        <p style={{ fontSize: '11px', color: 'var(--text-tertiary)', lineHeight: 1.5, marginBottom: 'var(--sp-3)' }}>
                          Severing this edge separates articulation points: {criticalityReport.articulation_points.join(', ')}.
                        </p>
                        <button
                          onClick={() => addNotification({ type: 'warning', title: 'Edge Highlighted', message: `${criticalityReport.bridges[0] || 'E-088'} marked on spatial canvas.` })}
                          className="btn-tactical"
                          style={{ width: '100%', justifyContent: 'center', fontSize: '11px' }}
                        >
                          Focus on Map
                        </button>
                      </div>

                      <div className="glass-card" style={{ padding: 'var(--sp-4)', borderRadius: 'var(--radius-md)' }}>
                        <div className="section-header">Critical Nodes</div>
                        {criticalityReport.top_critical_nodes.map((node, i) => (
                          <MetricRow key={node.id} label={`#${i + 1} ${node.id}`} value={node.score.toFixed(2)} color={i === 0 ? 'var(--critical)' : i === 1 ? 'var(--warning)' : 'var(--primary-500)'} />
                        ))}
                      </div>
                    </>
                  ) : (
                    <EmptyState
                      icon={<AlertTriangle size={20} />}
                      title="No Criticality Data"
                      description="Run centrality analysis to identify bottleneck nodes, bridges, and vulnerability scores in the network."
                      action={{ label: 'Run Analysis', onClick: triggerCriticality }}
                    />
                  )}
                </>
              )}

              {/* ── SIMULATION & DECISION SUPPORT ── */}
              {(activeView === 'simulation' || activeView === 'decision-support') && (
                <>
                  <button
                    disabled={isLoadingAction}
                    onClick={triggerSimulation}
                    className="btn-tactical"
                    style={{ width: '100%', justifyContent: 'center', background: 'rgba(239,68,68,0.2)', borderColor: 'var(--critical)', color: 'var(--critical)' }}
                  >
                    <Play size={13} /> {isLoadingAction ? 'Simulating...' : 'Trigger Disaster Blast'}
                  </button>

                  {simulationResult ? (
                    <>
                      <div className="glass-card" style={{ padding: 'var(--sp-4)', borderRadius: 'var(--radius-md)', borderLeft: '3px solid var(--critical)' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--critical)', fontWeight: 700, fontSize: '13px', marginBottom: '8px' }}>
                          <ShieldAlert size={15} /> Disruption Telemetry
                        </div>
                        <MetricRow label="Efficiency Drop" value={`${simulationResult.efficiency_drop_pct}%`} color="var(--critical)" />
                        <MetricRow label="Disconnected Nodes" value={String(simulationResult.disconnected_nodes)} color="var(--warning)" />
                        <MetricRow label="Detour Factor" value={`${simulationResult.detour_factor}x`} color="#FBBF24" />
                      </div>

                      <div className="glass-card" style={{ padding: 'var(--sp-4)', borderRadius: 'var(--radius-md)', borderLeft: '3px solid var(--success)' }}>
                        <div className="section-header" style={{ color: 'var(--success)' }}>AI Repair Priority</div>
                        <div style={{ padding: 'var(--sp-3)', background: 'rgba(16,185,129,0.06)', borderRadius: 'var(--radius-sm)', border: '1px solid rgba(16,185,129,0.15)' }}>
                          <div style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '2px' }}>
                            #1 Deploy Modular Link at RH-001
                          </div>
                          <div style={{ fontSize: '10px', color: 'var(--success)' }}>
                            Restores LCC (+16.1% resilience boost)
                          </div>
                        </div>
                      </div>
                    </>
                  ) : (
                    <EmptyState
                      icon={<Activity size={20} />}
                      title="No Simulation Run"
                      description="Trigger a disaster stress blast to model infrastructure failure and evaluate network resilience under extreme conditions."
                      action={{ label: 'Start Simulation', onClick: triggerSimulation }}
                    />
                  )}
                </>
              )}

              {/* ── CONFIG ── */}
              {activeView === 'config' && (
                <div className="glass-card" style={{ padding: 'var(--sp-4)', borderRadius: 'var(--radius-md)', display: 'flex', flexDirection: 'column', gap: 'var(--sp-3)' }}>
                  <div className="section-header">System Parameters</div>
                  <div>
                    <label style={{ fontSize: '11px', color: 'var(--text-tertiary)', display: 'block', marginBottom: '4px' }}>Backend Endpoint</label>
                    <input type="text" readOnly defaultValue="http://127.0.0.1:8000/api/v1" className="font-mono" style={{ width: '100%', padding: '7px 10px', background: 'rgba(0,0,0,0.3)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-sm)', color: 'var(--text-secondary)', fontSize: '11px' }} />
                  </div>
                  <MetricRow label="AI Threshold" value={systemConfig.ai_confidence_threshold.toFixed(2)} color="#7F00FF" />
                  <MetricRow label="RDP Epsilon" value={`${systemConfig.rdp_epsilon.toFixed(1)} px`} color="#3B82F6" />
                  <MetricRow label="Backend Status" value={backendHealth === 'healthy' ? 'Connected' : 'Offline'} color={backendHealth === 'healthy' ? 'var(--success)' : 'var(--warning)'} />
                  <button
                    onClick={() => { initBackendSync(); addNotification({ type: 'info', title: 'Reconnecting', message: 'Attempting to re-establish backend connection...' }); }}
                    className="btn-tactical"
                    style={{ justifyContent: 'center', width: '100%' }}
                  >
                    <RefreshCw size={13} /> Reconnect Backend
                  </button>
                </div>
              )}

            </motion.div>
          </AnimatePresence>
        </div>
      )}
    </div>
  );
};
