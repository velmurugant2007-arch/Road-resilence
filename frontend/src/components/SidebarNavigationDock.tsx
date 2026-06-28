import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useAppStore, type DashboardView } from '../store/useAppStore';
import { 
  LayoutDashboard, 
  Cpu, 
  Share2, 
  HeartHandshake, 
  AlertTriangle, 
  Activity, 
  CheckSquare, 
  Sliders,
  ChevronRight,
  ChevronLeft
} from 'lucide-react';

const navItems: { view: DashboardView; label: string; icon: React.ReactNode }[] = [
  { view: 'overview', label: 'Overview', icon: <LayoutDashboard size={20} /> },
  { view: 'ai-extraction', label: 'AI Road Extraction', icon: <Cpu size={20} /> },
  { view: 'graph-construction', label: 'Graph Construction', icon: <Share2 size={20} /> },
  { view: 'graph-healing', label: 'Graph Healing (XAI)', icon: <HeartHandshake size={20} /> },
  { view: 'criticality', label: 'Criticality Analysis', icon: <AlertTriangle size={20} /> },
  { view: 'simulation', label: 'Stress Simulation', icon: <Activity size={20} /> },
  { view: 'decision-support', label: 'Decision Support', icon: <CheckSquare size={20} /> },
  { view: 'config', label: 'System Configuration', icon: <Sliders size={20} /> },
];

export const SidebarNavigationDock: React.FC = () => {
  const [isExpanded, setIsExpanded] = useState(false);
  const { activeView, setActiveView } = useAppStore();

  return (
    <motion.nav
      initial={{ width: '64px' }}
      animate={{ width: isExpanded ? '220px' : '64px' }}
      transition={{ type: 'spring', stiffness: 260, damping: 28 }}
      className="glass-panel"
      style={{
        position: 'fixed',
        top: '92px',
        left: '24px',
        bottom: '24px',
        borderRadius: '20px',
        display: 'flex',
        flexDirection: 'column',
        padding: '16px 10px',
        zIndex: 400,
        overflow: 'hidden'
      }}
    >
      {/* Toggle Expansion Button */}
      <div style={{ display: 'flex', justifyContent: isExpanded ? 'flex-end' : 'center', marginBottom: '16px' }}>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          style={{
            background: 'rgba(255, 255, 255, 0.05)',
            border: '1px solid var(--border-subtle)',
            borderRadius: '50%',
            width: '32px',
            height: '32px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--text-secondary)',
            cursor: 'pointer'
          }}
        >
          {isExpanded ? <ChevronLeft size={16} /> : <ChevronRight size={16} />}
        </button>
      </div>

      {/* Nav List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', flex: 1 }}>
        {navItems.map((item) => {
          const isActive = activeView === item.view;
          return (
            <button
              key={item.view}
              onClick={() => setActiveView(item.view)}
              title={!isExpanded ? item.label : undefined}
              style={{
                position: 'relative',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px',
                borderRadius: '12px',
                background: isActive ? 'rgba(0, 242, 254, 0.15)' : 'transparent',
                border: 'none',
                color: isActive ? 'var(--primary-500)' : 'var(--text-secondary)',
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'all 0.15s ease'
              }}
            >
              {/* Active neon indicator */}
              {isActive && (
                <motion.div
                  layoutId="activeNavIndicator"
                  style={{
                    position: 'absolute',
                    left: '0',
                    top: '8px',
                    bottom: '8px',
                    width: '3px',
                    backgroundColor: 'var(--primary-500)',
                    borderRadius: '2px',
                    boxShadow: '0 0 8px var(--primary-500)'
                  }}
                />
              )}
              
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minWidth: '24px' }}>
                {item.icon}
              </div>

              {isExpanded && (
                <span style={{
                  fontSize: '13px',
                  fontWeight: isActive ? 600 : 400,
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis'
                }}>
                  {item.label}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Bottom Status */}
      {isExpanded && (
        <div style={{
          padding: '12px',
          background: 'rgba(0,0,0,0.2)',
          borderRadius: '10px',
          fontSize: '11px',
          color: 'var(--text-tertiary)'
        }}>
          <div>ISRO Hackathon PS-4</div>
          <div style={{ color: 'var(--primary-500)', fontWeight: 600 }}>v1.0.0-PROD</div>
        </div>
      )}
    </motion.nav>
  );
};
