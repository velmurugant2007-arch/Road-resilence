import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

const logs = [
  '[0.02s] Initializing CartoDB Dark Matter WebGL canvas...',
  '[0.08s] Fetching pre-computed Hero City graph topology...',
  '[0.12s] Mounting SegFormer AI tensor inference shaders...',
  '[0.18s] Synchronizing XAI repair explanation metadata layer...',
  '[READY] ATLAS Command System Operational.'
];

export const TacticalLoader: React.FC<{ onComplete: () => void }> = ({ onComplete }) => {
  const [logIndex, setLogIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setLogIndex((prev) => {
        if (prev < logs.length - 1) {
          return prev + 1;
        } else {
          clearInterval(timer);
          setTimeout(onComplete, 600);
          return prev;
        }
      });
    }, 400);

    return () => clearInterval(timer);
  }, [onComplete]);

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      backgroundColor: '#05070A',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 9999
    }}>
      {/* Radar Sweep Container */}
      <div style={{ position: 'relative', width: '180px', height: '180px', marginBottom: '40px' }}>
        {/* Concentric Circles */}
        <div style={{
          position: 'absolute', inset: '0', borderRadius: '50%', border: '1px solid rgba(0, 242, 254, 0.2)'
        }} />
        <div style={{
          position: 'absolute', inset: '30px', borderRadius: '50%', border: '1px dashed rgba(0, 242, 254, 0.3)'
        }} />
        <div style={{
          position: 'absolute', inset: '60px', borderRadius: '50%', border: '1px solid rgba(0, 242, 254, 0.4)'
        }} />
        <div style={{
          position: 'absolute', inset: '86px', borderRadius: '50%', backgroundColor: '#00F2FE', boxShadow: '0 0 15px #00F2FE'
        }} />

        {/* Rotating Radar Line */}
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          style={{
            position: 'absolute',
            top: '0',
            left: '50%',
            width: '50%',
            height: '50%',
            transformOrigin: 'bottom left',
            background: 'linear-gradient(135deg, rgba(0, 242, 254, 0.8) 0%, rgba(0, 242, 254, 0) 80%)',
            borderRight: '2px solid #00F2FE',
            borderTopRightRadius: '100%'
          }}
        />
      </div>

      <h1 style={{ color: '#FFFFFF', fontSize: '24px', letterSpacing: '2px', marginBottom: '8px' }}>
        ATLAS COMMAND SYSTEM
      </h1>
      <p style={{ color: '#00F2FE', fontSize: '12px', fontWeight: 600, letterSpacing: '4px', marginBottom: '24px' }}>
        ISRO BHUvan GEOSPATIAL INTELLIGENCE
      </p>

      {/* Terminal Log Output */}
      <div style={{
        width: '440px',
        background: 'rgba(15, 23, 42, 0.6)',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        borderRadius: '8px',
        padding: '16px',
        fontFamily: "'Roboto Mono', monospace",
        fontSize: '12px',
        color: '#A7F3D0',
        minHeight: '120px'
      }}>
        {logs.slice(0, logIndex + 1).map((log, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.2 }}
            style={{ marginBottom: '6px', color: idx === logIndex ? '#00F2FE' : 'rgba(255, 255, 255, 0.7)' }}
          >
            {log}
          </motion.div>
        ))}
      </div>
    </div>
  );
};
