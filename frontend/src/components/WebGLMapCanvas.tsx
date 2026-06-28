import React from 'react';
import { useAppStore } from '../store/useAppStore';

export const WebGLMapCanvas: React.FC = () => {
  const { activeView, setSelectedRepairId, setActiveView, addNotification, isSimulating } = useAppStore();

  const handleHealedClick = (id: string) => {
    setSelectedRepairId(id);
    setActiveView('graph-healing');
    addNotification({
      type: 'success',
      title: `Selected Repair: ${id}`,
      message: `Inspecting multi-factor hybrid cost breakdown for ${id}.`
    });
  };

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      backgroundColor: 'var(--bg-canvas)',
      zIndex: 0,
      overflow: 'hidden'
    }}>
      {/* Dark Matter Grid Basemap Simulation */}
      <div style={{
        position: 'absolute',
        inset: 0,
        backgroundImage: 'radial-gradient(rgba(0, 242, 254, 0.08) 1px, transparent 0)',
        backgroundSize: '40px 40px',
        opacity: 0.8
      }} />

      {/* SVG Spatial Canvas Overlay */}
      <svg
        style={{ width: '100%', height: '100%', position: 'absolute', inset: 0 }}
        viewBox="0 0 1440 900"
        preserveAspectRatio="xMidYMid slice"
      >
        <defs>
          {/* Cyan Neon Glow Filter */}
          <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>

          <filter id="green-glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="5" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>

          <filter id="red-glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="8" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* Baseline Road Polylines (White/Blue tactical vectors) */}
        <g opacity={activeView === 'ai-extraction' ? 0.4 : 0.85}>
          <path d="M 100,200 L 400,250 L 700,220 L 1100,300 L 1350,280" stroke="#38BDF8" strokeWidth="3" fill="none" />
          <path d="M 300,800 L 450,550 L 700,220 L 850,500 L 1200,750" stroke="#38BDF8" strokeWidth="4" fill="none" />
          <path d="M 200,450 L 450,550 L 850,500 L 1100,520" stroke="#93C5FD" strokeWidth="2.5" fill="none" strokeDasharray={activeView === 'graph-construction' ? "6,6" : "none"} />
          <path d="M 600,100 L 650,400 L 850,500 L 900,850" stroke="#38BDF8" strokeWidth="3.5" fill="none" />
        </g>

        {/* Cloud Occlusion Masks (AI Extraction View) */}
        {activeView === 'ai-extraction' && (
          <g opacity="0.65">
            <ellipse cx="580" cy="360" rx="140" ry="90" fill="#7F00FF" filter="url(#neon-glow)" />
            <ellipse cx="950" cy="480" rx="110" ry="70" fill="#E100FF" filter="url(#neon-glow)" />
            <text x="530" y="365" fill="#FFF" fontSize="14" fontWeight="bold" fontFamily="'Outfit', sans-serif">CLOUD OCCLUSION (92%)</text>
            <text x="900" y="485" fill="#FFF" fontSize="14" fontWeight="bold" fontFamily="'Outfit', sans-serif">CANOPY MASK (88%)</text>
          </g>
        )}

        {/* Disaster Flood Blast Zone (Simulation View) */}
        {(activeView === 'simulation' || activeView === 'decision-support' || isSimulating) && (
          <g>
            <circle cx="700" cy="220" r="120" fill="rgba(239, 68, 68, 0.25)" stroke="#EF4444" strokeWidth="2" strokeDasharray="8,4" filter="url(#red-glow)">
              <animate attributeName="r" values="110;130;110" dur="3s" repeatCount="indefinite" />
            </circle>
            <text x="630" y="160" fill="#EF4444" fontSize="16" fontWeight="bold" letterSpacing="2">500mm FLOOD INUNDATION</text>
            {/* Severed Bridge Icon */}
            <line x1="670" y1="200" x2="730" y2="240" stroke="#EF4444" strokeWidth="6" />
            <line x1="730" y1="200" x2="670" y2="240" stroke="#EF4444" strokeWidth="6" />
          </g>
        )}

        {/* Healed Road Links (XAI Explainable Repairs) */}
        <g style={{ cursor: 'pointer' }} onClick={() => handleHealedClick('RH-001')}>
          {/* RH-001 Pulsating Green Link */}
          <line
            x1="450" y1="550" x2="650" y2="400"
            stroke="#10B981" strokeWidth="5" strokeDasharray="10,6"
            filter="url(#green-glow)"
          >
            <animate attributeName="stroke-dashoffset" from="16" to="0" dur="1s" repeatCount="indefinite" />
          </line>
          <circle cx="550" cy="475" r="16" fill="#10B981" filter="url(#green-glow)" />
          <text x="528" y="480" fill="#000" fontSize="11" fontWeight="bold" className="font-mono">RH-001</text>
        </g>

        {/* Junction Nodes */}
        <g>
          {[
            { id: 'N154', x: 450, y: 550, color: '#00F2FE' },
            { id: 'N173', x: 650, y: 400, color: '#00F2FE' },
            { id: 'N101', x: 700, y: 220, color: (activeView === 'simulation' || isSimulating) ? '#EF4444' : '#00F2FE' },
            { id: 'N204', x: 850, y: 500, color: activeView === 'criticality' ? '#F59E0B' : '#00F2FE' },
          ].map((node) => (
            <g key={node.id} style={{ cursor: 'pointer' }} onClick={() => addNotification({ type: 'info', title: `Node ${node.id}`, message: `Coordinates: (${node.x}, ${node.y}). Degree: 4.` })}>
              <circle cx={node.x} cy={node.y} r="8" fill={node.color} filter="url(#neon-glow)" />
              <circle cx={node.x} cy={node.y} r="14" fill="none" stroke={node.color} strokeWidth="1.5" opacity="0.6" />
              <text x={node.x + 16} y={node.y + 4} fill="#FFF" fontSize="12" fontWeight="600" className="font-mono" style={{ textShadow: '0 2px 4px #000' }}>
                {node.id}
              </text>
            </g>
          ))}
        </g>
      </svg>

      {/* Bottom Center Map Attribution */}
      <div style={{ position: 'absolute', bottom: '8px', right: '440px', fontSize: '10px', color: 'var(--text-disabled)', fontFamily: "'Roboto Mono', monospace", zIndex: 10 }}>
        © ISRO NRSC | Bhuvan WebGL Engine | CartoDB Dark Matter
      </div>
    </div>
  );
};
