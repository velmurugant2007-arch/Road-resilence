import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useAppStore, type DashboardView } from '../store/useAppStore';
import { 
  LayoutDashboard, Cpu, Share2, HeartHandshake, 
  AlertTriangle, Activity, CheckSquare, Sliders,
  ChevronRight, ChevronLeft
} from 'lucide-react';

const navItems: { view: DashboardView; label: string; icon: React.ReactNode; accent: string }[] = [
  { view: 'overview', label: 'Overview', icon: <LayoutDashboard size={18} />, accent: 'var(--primary-500)' },
  { view: 'ai-extraction', label: 'AI Extraction', icon: <Cpu size={18} />, accent: '#7F00FF' },
  { view: 'graph-construction', label: 'Vectorization', icon: <Share2 size={18} />, accent: '#3B82F6' },
  { view: 'graph-healing', label: 'Graph Healing', icon: <HeartHandshake size={18} />, accent: 'var(--success)' },
  { view: 'criticality', label: 'Criticality', icon: <AlertTriangle size={18} />, accent: 'var(--warning)' },
  { view: 'simulation', label: 'Simulation', icon: <Activity size={18} />, accent: 'var(--critical)' },
  { view: 'decision-support', label: 'Decisions', icon: <CheckSquare size={18} />, accent: 'var(--success)' },
  { view: 'config', label: 'Config', icon: <Sliders size={18} />, accent: 'var(--primary-500)' },
];

export const SidebarNavigationDock: React.FC = () => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [hoveredView, setHoveredView] = useState<DashboardView | null>(null);
  const { activeView, setActiveView } = useAppStore();

  return (
    <motion.nav
      initial={{ width: '60px' }}
      animate={{ width: isExpanded ? '200px' : '60px' }}
      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      className="glass-panel"
      style={{
        position: 'fixed',
        top: '88px',
        left: 'var(--sp-6)',
        bottom: 'var(--sp-6)',
        borderRadius: 'var(--radius-xl)',
        display: 'flex',
        flexDirection: 'column',
        padding: 'var(--sp-3) var(--sp-2)',
        zIndex: 400,
        overflow: 'hidden',
      }}
    >
      {/* Toggle */}
      <div style={{ display: 'flex', justifyContent: isExpanded ? 'flex-end' : 'center', marginBottom: 'var(--sp-3)', paddingRight: isExpanded ? '4px' : 0 }}>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="icon-btn"
          style={{ width: '28px', height: '28px', borderRadius: '50%' }}
        >
          {isExpanded ? <ChevronLeft size={14} /> : <ChevronRight size={14} />}
        </button>
      </div>

      {/* Nav Items */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', flex: 1 }}>
        {navItems.map((item) => {
          const isActive = activeView === item.view;
          const isHovered = hoveredView === item.view;
          return (
            <motion.button
              key={item.view}
              onClick={() => setActiveView(item.view)}
              onMouseEnter={() => setHoveredView(item.view)}
              onMouseLeave={() => setHoveredView(null)}
              title={!isExpanded ? item.label : undefined}
              whileTap={{ scale: 0.95 }}
              style={{
                position: 'relative',
                display: 'flex',
                alignItems: 'center',
                gap: 'var(--sp-3)',
                padding: '10px 12px',
                borderRadius: 'var(--radius-md)',
                background: isActive ? `${item.accent}15` : isHovered ? 'rgba(255,255,255,0.04)' : 'transparent',
                border: 'none',
                color: isActive ? item.accent : isHovered ? 'var(--text-primary)' : 'var(--text-tertiary)',
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'color var(--duration-fast), background var(--duration-fast)',
              }}
            >
              {/* Active Indicator */}
              {isActive && (
                <motion.div
                  layoutId="sidebarIndicator"
                  style={{
                    position: 'absolute', left: '0', top: '10px', bottom: '10px',
                    width: '3px', backgroundColor: item.accent,
                    borderRadius: '0 2px 2px 0',
                    boxShadow: `0 0 8px ${item.accent}`,
                  }}
                  transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                />
              )}
              
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minWidth: '20px', flexShrink: 0 }}>
                {item.icon}
              </div>

              {isExpanded && (
                <motion.span
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.05 }}
                  style={{
                    fontSize: '12px',
                    fontWeight: isActive ? 600 : 400,
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                  }}
                >
                  {item.label}
                </motion.span>
              )}
            </motion.button>
          );
        })}
      </div>

      {/* Footer */}
      {isExpanded && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          style={{
            padding: 'var(--sp-3)',
            background: 'rgba(0,0,0,0.15)',
            borderRadius: 'var(--radius-sm)',
            fontSize: '10px',
            color: 'var(--text-disabled)',
          }}
        >
          <div>ISRO Hackathon PS-4</div>
          <div style={{ color: 'var(--primary-500)', fontWeight: 600, fontSize: '10px' }}>v1.0.0</div>
        </motion.div>
      )}
    </motion.nav>
  );
};
