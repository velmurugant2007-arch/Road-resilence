import React from 'react';
import { useAppStore } from '../store/useAppStore';
import { FileText, Camera, Download, Settings, Bell, Command, Sun, Moon } from 'lucide-react';

export const TopTelemetryBar: React.FC = () => {
  const { 
    setCommandPaletteOpen, 
    setNotificationOpen, 
    notifications, 
    setActiveView,
    addNotification,
    theme,
    setTheme,
    backendHealth,
    triggerExportGeoJson
  } = useAppStore();

  const unreadCount = notifications.filter(n => !n.read).length;

  const handleAction = (actionName: string) => {
    if (actionName === 'Export Report' || actionName === 'Generate PDF') {
      triggerExportGeoJson();
      return;
    }
    if (actionName === 'Capture Screenshot') {
      window.print();
    }
    addNotification({
      type: 'success',
      title: `${actionName} Executed`,
      message: `Successfully triggered ${actionName.toLowerCase()} presentation action.`
    });
  };

  const getHealthBadge = () => {
    if (backendHealth === 'healthy') {
      return { text: 'API: HEALTHY (<50ms)', bg: 'var(--primary-900)', border: 'var(--primary-500)', dot: 'var(--primary-500)' };
    }
    if (backendHealth === 'offline') {
      return { text: 'API: OFFLINE CACHE', bg: 'rgba(245, 158, 11, 0.15)', border: '#F59E0B', dot: '#F59E0B' };
    }
    return { text: 'API: SYNCING...', bg: 'rgba(100, 116, 139, 0.15)', border: '#64748B', dot: '#64748B' };
  };

  const healthStyle = getHealthBadge();

  return (
    <header className="glass-panel" style={{
      position: 'fixed',
      top: '16px',
      left: '24px',
      right: '24px',
      height: '56px',
      borderRadius: '14px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 20px',
      zIndex: 400
    }}>
      {/* Left Branding */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer' }} onClick={() => setActiveView('overview')}>
        <div style={{
          width: '32px', height: '32px', borderRadius: '8px',
          background: 'linear-gradient(135deg, #00F2FE 0%, #003B46 100%)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          color: '#000', fontWeight: 'bold', fontSize: '16px', fontFamily: "'Outfit', sans-serif"
        }}>
          A
        </div>
        <div>
          <span style={{ fontSize: '16px', fontWeight: 700, letterSpacing: '1.5px', color: 'var(--text-primary)' }}>ATLAS</span>
          <span style={{ marginLeft: '8px', fontSize: '12px', color: 'var(--primary-500)', fontWeight: 600 }}>
            ISRO ROUTE RESILIENCE
          </span>
        </div>
      </div>

      {/* Center Command Trigger & Health Pill */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <button
          onClick={() => setCommandPaletteOpen(true)}
          style={{
            background: 'rgba(255, 255, 255, 0.05)',
            border: '1px solid var(--border-subtle)',
            borderRadius: '6px',
            padding: '6px 12px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            color: 'var(--text-secondary)',
            fontSize: '12px',
            cursor: 'pointer'
          }}
        >
          <Command size={14} color="var(--primary-500)" />
          <span>Search command palette...</span>
          <kbd style={{
            background: 'rgba(255, 255, 255, 0.1)',
            padding: '2px 6px',
            borderRadius: '4px',
            fontSize: '10px',
            color: 'var(--text-primary)'
          }}>Ctrl+K</kbd>
        </button>

        <div style={{
          background: healthStyle.bg,
          border: `1px solid ${healthStyle.border}`,
          borderRadius: '9999px',
          padding: '4px 12px',
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          fontSize: '11px',
          fontWeight: 600,
          color: 'var(--text-primary)'
        }}>
          <span style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: healthStyle.dot, boxShadow: `0 0 6px ${healthStyle.dot}` }} />
          <span>{healthStyle.text}</span>
        </div>
      </div>

      {/* Right Presentation Actions */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <button
          onClick={() => handleAction('Export Report')}
          title="Export Report"
          className="btn-tactical"
          style={{ padding: '6px 12px', fontSize: '12px' }}
        >
          <FileText size={14} />
          <span>Export Report</span>
        </button>

        <button
          onClick={() => handleAction('Capture Screenshot')}
          title="Capture Screenshot"
          style={{
            background: 'transparent', border: '1px solid var(--border-subtle)',
            borderRadius: '6px', padding: '6px', color: 'var(--text-secondary)', cursor: 'pointer'
          }}
        >
          <Camera size={16} />
        </button>

        <button
          onClick={() => handleAction('Generate PDF')}
          title="Generate PDF"
          style={{
            background: 'transparent', border: '1px solid var(--border-subtle)',
            borderRadius: '6px', padding: '6px', color: 'var(--text-secondary)', cursor: 'pointer'
          }}
        >
          <Download size={16} />
        </button>

        <button
          onClick={() => setActiveView('config')}
          title="Settings"
          style={{
            background: 'transparent', border: '1px solid var(--border-subtle)',
            borderRadius: '6px', padding: '6px', color: 'var(--text-secondary)', cursor: 'pointer'
          }}
        >
          <Settings size={16} />
        </button>

        <button
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          title="Toggle Theme"
          style={{
            background: 'transparent', border: '1px solid var(--border-subtle)',
            borderRadius: '6px', padding: '6px', color: 'var(--text-secondary)', cursor: 'pointer'
          }}
        >
          {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
        </button>

        {/* Notification Bell */}
        <button
          onClick={() => setNotificationOpen(true)}
          style={{
            position: 'relative',
            background: 'rgba(255, 255, 255, 0.05)',
            border: '1px solid var(--border-subtle)',
            borderRadius: '6px', padding: '6px', color: 'var(--text-primary)', cursor: 'pointer',
            marginLeft: '4px'
          }}
        >
          <Bell size={16} />
          {unreadCount > 0 && (
            <span style={{
              position: 'absolute', top: '-4px', right: '-4px',
              backgroundColor: 'var(--critical)', color: '#FFF',
              fontSize: '10px', fontWeight: 'bold', width: '16px', height: '16px',
              borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              {unreadCount}
            </span>
          )}
        </button>
      </div>
    </header>
  );
};
