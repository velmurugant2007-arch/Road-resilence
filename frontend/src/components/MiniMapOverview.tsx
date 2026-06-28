import React from 'react';
import { useAppStore } from '../store/useAppStore';
import { Navigation, MapPin } from 'lucide-react';

export const MiniMapOverview: React.FC = () => {
  const { activeView, isSimulating } = useAppStore();

  return (
    <div className="glass-panel" style={{
      position: 'fixed',
      bottom: '100px',
      left: '104px',
      width: '220px',
      height: '160px',
      borderRadius: '14px',
      padding: '10px',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      zIndex: 300,
      pointerEvents: 'none'
    }}>
      {/* Top Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ fontSize: '10px', fontWeight: 700, letterSpacing: '1px', color: 'var(--text-secondary)' }}>
          OVERVIEW MINI MAP
        </span>
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '10px', color: 'var(--primary-500)' }}>
          <Navigation size={10} />
          <span className="font-mono">12.91°N</span>
        </div>
      </div>

      {/* Mini Map Spatial Graphic */}
      <div style={{
        position: 'relative',
        flex: 1,
        margin: '8px 0',
        backgroundColor: '#05070A',
        borderRadius: '6px',
        border: '1px solid var(--border-subtle)',
        overflow: 'hidden'
      }}>
        {/* Grid lines */}
        <div style={{ position: 'absolute', inset: 0, backgroundImage: 'radial-gradient(rgba(255,255,255,0.1) 1px, transparent 0)', backgroundSize: '12px 12px' }} />

        {/* Hero City Extent Box */}
        <div style={{
          position: 'absolute',
          inset: '16px',
          border: '1px dashed var(--primary-500)',
          borderRadius: '4px',
          opacity: 0.6
        }} />

        {/* Disaster Blast Region (if simulation or criticality active) */}
        {(activeView === 'simulation' || activeView === 'decision-support' || isSimulating) && (
          <div style={{
            position: 'absolute',
            top: '40%',
            left: '45%',
            width: '30px',
            height: '30px',
            backgroundColor: 'rgba(239, 68, 68, 0.4)',
            border: '1px solid var(--critical)',
            borderRadius: '50%',
            transform: 'translate(-50%, -50%)',
            boxShadow: '0 0 8px var(--critical)'
          }} />
        )}

        {/* Current Camera Viewport Rectangle */}
        <div style={{
          position: 'absolute',
          top: '30%',
          left: '35%',
          width: '60px',
          height: '45px',
          border: '2px solid #FFFFFF',
          backgroundColor: 'rgba(255, 255, 255, 0.1)',
          borderRadius: '2px',
          boxShadow: '0 0 6px rgba(255,255,255,0.5)'
        }} />

        {/* Camera Pin */}
        <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: 'var(--primary-500)' }}>
          <MapPin size={12} fill="var(--primary-500)" />
        </div>
      </div>

      {/* Bottom Telemetry Footer */}
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '9px', color: 'var(--text-tertiary)', fontFamily: "'Roboto Mono', monospace" }}>
        <span>EXTENT: 8x8 GRID</span>
        <span>CAM: ZOOM 14.2</span>
      </div>
    </div>
  );
};
