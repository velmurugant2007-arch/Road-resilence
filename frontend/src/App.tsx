import { useState, useEffect } from 'react';
import { useAppStore } from './store/useAppStore';
import { TacticalLoader } from './components/TacticalLoader';
import { TopTelemetryBar } from './components/TopTelemetryBar';
import { SidebarNavigationDock } from './components/SidebarNavigationDock';
import { WebGLMapCanvas } from './components/WebGLMapCanvas';
import { FloatingInspectorPanel } from './components/FloatingInspectorPanel';
import { SimulationTimelineHUD } from './components/SimulationTimelineHUD';
import { MiniMapOverview } from './components/MiniMapOverview';
import { CommandPaletteModal } from './components/CommandPaletteModal';
import { NotificationCenterDrawer } from './components/NotificationCenterDrawer';

export default function App() {
  const [isBooting, setIsBooting] = useState(true);
  const { initBackendSync } = useAppStore();

  useEffect(() => {
    initBackendSync();
  }, [initBackendSync]);

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative', overflow: 'hidden' }}>
      {isBooting ? (
        <TacticalLoader onComplete={() => setIsBooting(false)} />
      ) : (
        <>
          {/* Spatial WebGL Map Canvas (70%+ screen budget) */}
          <WebGLMapCanvas />

          {/* HUD Navigation Header */}
          <TopTelemetryBar />

          {/* Left Navigation Dock */}
          <SidebarNavigationDock />

          {/* Bottom Left Mini Map */}
          <MiniMapOverview />

          {/* Bottom Simulation Scrubbing HUD */}
          <SimulationTimelineHUD />

          {/* Right Inspector & Analytics Panel */}
          <FloatingInspectorPanel />

          {/* Floating Command Palette (Ctrl+K) */}
          <CommandPaletteModal />

          {/* Slide-out Notification Center Drawer */}
          <NotificationCenterDrawer />
        </>
      )}
    </div>
  );
}
