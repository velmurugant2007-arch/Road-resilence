import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, AlertTriangle, Info, XCircle, X } from 'lucide-react';
import { useAppStore, type NotificationItem } from '../store/useAppStore';

const TOAST_DURATION = 4500;

const iconMap = {
  success: <CheckCircle2 size={16} />,
  warning: <AlertTriangle size={16} />,
  info: <Info size={16} />,
  critical: <XCircle size={16} />,
};

const accentMap = {
  success: '#10B981',
  warning: '#F59E0B',
  info: '#3B82F6',
  critical: '#EF4444',
};

export const ToastStack: React.FC = () => {
  const { notifications } = useAppStore();
  const [visibleToasts, setVisibleToasts] = useState<NotificationItem[]>([]);
  const [dismissed, setDismissed] = useState<Set<string>>(new Set());

  useEffect(() => {
    if (notifications.length > 0) {
      const latest = notifications[0];
      if (!visibleToasts.find(t => t.id === latest.id) && !dismissed.has(latest.id)) {
        setVisibleToasts(prev => [latest, ...prev].slice(0, 4));
        const timer = setTimeout(() => {
          setVisibleToasts(prev => prev.filter(t => t.id !== latest.id));
        }, TOAST_DURATION);
        return () => clearTimeout(timer);
      }
    }
  }, [notifications, visibleToasts, dismissed]);

  const dismissToast = (id: string) => {
    setDismissed(prev => new Set(prev).add(id));
    setVisibleToasts(prev => prev.filter(t => t.id !== id));
  };

  return (
    <div className="toast-container">
      <AnimatePresence mode="popLayout">
        {visibleToasts.map((toast) => {
          const accent = accentMap[toast.type];
          return (
            <motion.div
              key={toast.id}
              layout
              initial={{ opacity: 0, x: 24, scale: 0.96 }}
              animate={{ opacity: 1, x: 0, scale: 1 }}
              exit={{ opacity: 0, x: 24, scale: 0.96 }}
              transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] as const }}
              style={{
                pointerEvents: 'auto',
                background: 'var(--surface-3)',
                backdropFilter: 'blur(24px)',
                WebkitBackdropFilter: 'blur(24px)',
                border: '1px solid var(--border-strong)',
                borderLeft: `3px solid ${accent}`,
                borderRadius: 'var(--radius-md)',
                padding: '12px 16px',
                minWidth: '320px',
                maxWidth: '400px',
                display: 'flex',
                alignItems: 'flex-start',
                gap: '12px',
                boxShadow: '0 16px 32px -8px rgba(0, 0, 0, 0.6)',
                cursor: 'pointer',
              }}
              onClick={() => dismissToast(toast.id)}
            >
              <div style={{ color: accent, marginTop: '1px', flexShrink: 0 }}>
                {iconMap[toast.type]}
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '2px' }}>
                  {toast.title}
                </div>
                <div style={{ fontSize: '11px', color: 'var(--text-tertiary)', lineHeight: 1.4, overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical' as any }}>
                  {toast.message}
                </div>
              </div>
              <button
                onClick={(e) => { e.stopPropagation(); dismissToast(toast.id); }}
                style={{ background: 'none', border: 'none', color: 'var(--text-disabled)', cursor: 'pointer', padding: '2px', flexShrink: 0 }}
              >
                <X size={12} />
              </button>
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
};
