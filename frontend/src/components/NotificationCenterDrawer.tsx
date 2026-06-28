import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAppStore } from '../store/useAppStore';
import { X, CheckCircle, AlertTriangle, Info, Bell, Trash2 } from 'lucide-react';

export const NotificationCenterDrawer: React.FC = () => {
  const { isNotificationOpen, setNotificationOpen, notifications, markAllNotificationsRead } = useAppStore();

  const getIcon = (type: string) => {
    switch (type) {
      case 'success': return <CheckCircle size={18} color="var(--success)" />;
      case 'warning': return <AlertTriangle size={18} color="var(--warning)" />;
      case 'critical': return <AlertTriangle size={18} color="var(--critical)" />;
      default: return <Info size={18} color="var(--info)" />;
    }
  };

  return (
    <AnimatePresence>
      {isNotificationOpen && (
        <div style={{ position: 'fixed', inset: 0, zIndex: 1000, pointerEvents: 'none' }}>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setNotificationOpen(false)}
            style={{ position: 'absolute', inset: 0, backgroundColor: 'rgba(0,0,0,0.4)', pointerEvents: 'auto' }}
          />

          {/* Drawer */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            className="glass-panel"
            style={{
              position: 'absolute', top: '16px', right: '24px', bottom: '24px', width: '380px',
              borderRadius: '16px', display: 'flex', flexDirection: 'column', pointerEvents: 'auto',
              border: '1px solid var(--border-strong)', overflow: 'hidden'
            }}
          >
            {/* Header */}
            <div style={{ padding: '16px 20px', borderBottom: '1px solid var(--border-subtle)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Bell size={18} color="var(--primary-500)" />
                <span style={{ fontSize: '16px', fontWeight: 700, fontFamily: "'Outfit', sans-serif" }}>System Notification Center</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <button
                  onClick={markAllNotificationsRead}
                  title="Mark all as read"
                  style={{ background: 'transparent', border: 'none', color: 'var(--text-tertiary)', cursor: 'pointer' }}
                >
                  <Trash2 size={16} />
                </button>
                <button
                  onClick={() => setNotificationOpen(false)}
                  style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer' }}
                >
                  <X size={20} />
                </button>
              </div>
            </div>

            {/* List */}
            <div style={{ flex: 1, overflowY: 'auto', padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {notifications.length === 0 ? (
                <div style={{ textAlign: 'center', color: 'var(--text-tertiary)', padding: '40px 0', fontSize: '13px' }}>
                  No system telemetry notifications logged.
                </div>
              ) : (
                notifications.map((n) => (
                  <div key={n.id} style={{
                    padding: '12px', borderRadius: '10px', background: n.read ? 'rgba(255,255,255,0.02)' : 'rgba(0, 242, 254, 0.08)',
                    border: `1px solid ${n.read ? 'var(--border-subtle)' : 'rgba(0, 242, 254, 0.3)'}`,
                    display: 'flex', gap: '12px'
                  }}>
                    <div style={{ paddingTop: '2px' }}>{getIcon(n.type)}</div>
                    <div style={{ flex: 1 }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                        <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-primary)' }}>{n.title}</span>
                        <span style={{ fontSize: '10px', color: 'var(--text-tertiary)', fontFamily: "'Roboto Mono', monospace" }}>{n.timestamp}</span>
                      </div>
                      <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: 1.4 }}>{n.message}</p>
                    </div>
                  </div>
                ))
              )}
            </div>

            {/* Footer */}
            <div style={{ padding: '12px 16px', background: 'rgba(0,0,0,0.3)', borderTop: '1px solid var(--border-subtle)', textAlign: 'center', fontSize: '11px', color: 'var(--text-tertiary)' }}>
              ISRO-Grade Audit Log Active
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};
