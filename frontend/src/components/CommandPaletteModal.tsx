import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAppStore } from '../store/useAppStore';
import { Search, Share2, HeartHandshake, Activity, FileText, ArrowRight } from 'lucide-react';

export const CommandPaletteModal: React.FC = () => {
  const { 
    isCommandPaletteOpen, 
    setCommandPaletteOpen, 
    setActiveView, 
    setSelectedEdgeId, 
    setSelectedRepairId,
    setSimulating,
    addNotification,
    triggerExportGeoJson
  } = useAppStore();

  const [searchQuery, setSearchQuery] = useState('');

  // Global Ctrl+K / Cmd+K listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setCommandPaletteOpen(!isCommandPaletteOpen);
      } else if (e.key === 'Escape' && isCommandPaletteOpen) {
        setCommandPaletteOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isCommandPaletteOpen, setCommandPaletteOpen]);

  if (!isCommandPaletteOpen) return null;

  const actions = [
    { id: 'view-healing', title: 'Navigate: Graph Healing (XAI)', category: 'Navigation', icon: <HeartHandshake size={16} />, run: () => setActiveView('graph-healing') },
    { id: 'view-sim', title: 'Navigate: Stress Simulation', category: 'Navigation', icon: <Activity size={16} />, run: () => setActiveView('simulation') },
    { id: 'view-crit', title: 'Navigate: Criticality Analysis', category: 'Navigation', icon: <Share2 size={16} />, run: () => setActiveView('criticality') },
    { id: 'sim-trigger', title: 'Action: Trigger Disaster Flood Simulation', category: 'Simulations', icon: <Activity size={16} color="var(--critical)" />, run: () => { setActiveView('simulation'); setSimulating(true); addNotification({ type: 'warning', title: 'Simulation Started', message: 'Stochastic flood failure model executing.' }); } },
    { id: 'export-geo', title: 'Action: Export GeoJSON Network', category: 'Actions', icon: <FileText size={16} />, run: () => triggerExportGeoJson() },
    { id: 'search-rh001', title: 'Inspect Repair ID: RH-001 [Accepted]', category: 'Spatial Search', icon: <HeartHandshake size={16} color="var(--success)" />, run: () => { setActiveView('graph-healing'); setSelectedRepairId('RH-001'); setSelectedEdgeId('RH-001'); } },
    { id: 'search-e088', title: 'Inspect Edge ID: E-088 [Critical Link]', category: 'Spatial Search', icon: <Share2 size={16} color="var(--warning)" />, run: () => { setActiveView('criticality'); setSelectedEdgeId('E-088'); } },
    { id: 'search-n154', title: 'Inspect Node ID: N154 [Junction]', category: 'Spatial Search', icon: <Share2 size={16} color="var(--info)" />, run: () => { setActiveView('overview'); } }
  ];

  const filteredActions = actions.filter(a => 
    a.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    a.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <AnimatePresence>
      <div style={{
        position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.6)',
        backdropFilter: 'blur(4px)', zIndex: 1000, display: 'flex', alignItems: 'flex-start',
        justifyContent: 'center', paddingTop: '120px'
      }} onClick={() => setCommandPaletteOpen(false)}>
        
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: -20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: -20 }}
          transition={{ duration: 0.15 }}
          onClick={(e) => e.stopPropagation()}
          className="glass-panel"
          style={{
            width: '560px', maxHeight: '480px', borderRadius: '16px',
            display: 'flex', flexDirection: 'column', overflow: 'hidden',
            border: '1px solid var(--border-strong)', boxShadow: '0 25px 50px -12px rgba(0,0,0,0.9)'
          }}
        >
          {/* Search Input Box */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '16px', borderBottom: '1px solid var(--border-subtle)' }}>
            <Search size={20} color="var(--primary-500)" />
            <input
              autoFocus
              type="text"
              placeholder="Type a command or search nodes (N154), edges (E-088), repair IDs (RH-001)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                flex: 1, background: 'transparent', border: 'none', outline: 'none',
                color: 'var(--text-primary)', fontSize: '14px', fontFamily: "'Inter', sans-serif"
              }}
            />
            <kbd style={{
              background: 'rgba(255,255,255,0.1)', padding: '2px 6px', borderRadius: '4px', fontSize: '11px', color: 'var(--text-tertiary)'
            }}>ESC</kbd>
          </div>

          {/* Results List */}
          <div style={{ padding: '8px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '4px', maxHeight: '380px' }}>
            {filteredActions.length === 0 ? (
              <div style={{ padding: '24px', textAlign: 'center', color: 'var(--text-tertiary)', fontSize: '13px' }}>
                No commands or spatial IDs found matching "{searchQuery}"
              </div>
            ) : (
              filteredActions.map((action) => (
                <button
                  key={action.id}
                  onClick={() => {
                    action.run();
                    setCommandPaletteOpen(false);
                  }}
                  style={{
                    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                    padding: '10px 12px', borderRadius: '8px', background: 'transparent',
                    border: 'none', color: 'var(--text-primary)', cursor: 'pointer', textAlign: 'left',
                    transition: 'background 0.1s ease'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.08)'}
                  onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    {action.icon}
                    <div>
                      <div style={{ fontSize: '13px', fontWeight: 500 }}>{action.title}</div>
                      <div style={{ fontSize: '11px', color: 'var(--text-tertiary)' }}>{action.category}</div>
                    </div>
                  </div>
                  <ArrowRight size={14} color="var(--text-tertiary)" />
                </button>
              ))
            )}
          </div>

          {/* Footer */}
          <div style={{
            padding: '8px 16px', background: 'rgba(0,0,0,0.3)', borderTop: '1px solid var(--border-subtle)',
            fontSize: '11px', color: 'var(--text-tertiary)', display: 'flex', justifyContent: 'space-between'
          }}>
            <span>Linear Command Palette</span>
            <span>Use ↑↓ arrows to navigate</span>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};
