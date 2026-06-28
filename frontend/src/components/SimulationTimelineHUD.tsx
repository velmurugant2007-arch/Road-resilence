import React from 'react';
import { useAppStore } from '../store/useAppStore';
import { Play, Pause, RotateCcw, FastForward } from 'lucide-react';

export const SimulationTimelineHUD: React.FC = () => {
  const { activeView, isSimulating, setSimulating, simulationStep, setSimulationStep, addNotification } = useAppStore();

  if (activeView !== 'simulation' && activeView !== 'decision-support') return null;

  const togglePlay = () => {
    const nextState = !isSimulating;
    setSimulating(nextState);
    if (nextState) {
      addNotification({ type: 'warning', title: 'Simulation Running', message: `Executing step ${simulationStep}/100 flood progression.` });
    }
  };

  const resetSim = () => {
    setSimulating(false);
    setSimulationStep(1);
    addNotification({ type: 'info', title: 'Simulation Reset', message: 'Restored baseline Hero City road graph.' });
  };

  return (
    <div className="glass-panel" style={{
      position: 'fixed',
      bottom: '24px',
      left: '50%',
      transform: 'translateX(-50%)',
      width: '540px',
      height: '64px',
      borderRadius: '32px',
      padding: '0 24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: '20px',
      zIndex: 350
    }}>
      {/* Controls */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <button
          onClick={resetSim}
          title="Reset"
          style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer' }}
        >
          <RotateCcw size={18} />
        </button>

        <button
          onClick={togglePlay}
          title={isSimulating ? "Pause" : "Play"}
          style={{
            width: '40px', height: '40px', borderRadius: '50%',
            background: isSimulating ? 'var(--warning)' : 'var(--primary-500)',
            border: 'none', color: '#000', display: 'flex', alignItems: 'center',
            justifyContent: 'center', cursor: 'pointer', boxShadow: '0 0 12px rgba(0, 242, 254, 0.4)'
          }}
        >
          {isSimulating ? <Pause size={18} fill="#000" /> : <Play size={18} fill="#000" style={{ marginLeft: '2px' }} />}
        </button>

        <button
          onClick={() => setSimulationStep(Math.min(100, simulationStep + 10))}
          title="Step Forward"
          style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer' }}
        >
          <FastForward size={18} />
        </button>
      </div>

      {/* Slider */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '4px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', fontFamily: "'Roboto Mono', monospace" }}>
          <span style={{ color: 'var(--text-secondary)' }}>FLOOD PROGRESSION</span>
          <span style={{ color: 'var(--primary-500)', fontWeight: 600 }}>T+{simulationStep} min ({simulationStep}%)</span>
        </div>
        <input
          type="range"
          min={1}
          max={100}
          value={simulationStep}
          onChange={(e) => setSimulationStep(Number(e.target.value))}
          style={{
            width: '100%', height: '4px', accentColor: 'var(--primary-500)',
            background: 'rgba(255,255,255,0.2)', borderRadius: '2px', cursor: 'pointer'
          }}
        />
      </div>

      {/* Speed Indicator */}
      <div style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-tertiary)', fontFamily: "'Roboto Mono', monospace" }}>
        2.0x
      </div>
    </div>
  );
};
