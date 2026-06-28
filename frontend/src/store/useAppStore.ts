import { create } from 'zustand';

export type DashboardView = 
  | 'overview'
  | 'ai-extraction'
  | 'graph-construction'
  | 'graph-healing'
  | 'criticality'
  | 'simulation'
  | 'decision-support'
  | 'config';

export interface NotificationItem {
  id: string;
  timestamp: string;
  type: 'info' | 'success' | 'warning' | 'critical';
  title: string;
  message: string;
  read: boolean;
}

interface AppState {
  activeView: DashboardView;
  setActiveView: (view: DashboardView) => void;

  theme: 'dark' | 'light';
  setTheme: (theme: 'dark' | 'light') => void;

  isCommandPaletteOpen: boolean;
  setCommandPaletteOpen: (open: boolean) => void;

  isNotificationOpen: boolean;
  setNotificationOpen: (open: boolean) => void;

  notifications: NotificationItem[];
  addNotification: (notification: Omit<NotificationItem, 'id' | 'timestamp' | 'read'>) => void;
  markAllNotificationsRead: () => void;

  selectedEdgeId: string | null;
  setSelectedEdgeId: (id: string | null) => void;

  selectedNodeId: string | null;
  setSelectedNodeId: (id: string | null) => void;

  selectedRepairId: string | null;
  setSelectedRepairId: (id: string | null) => void;

  isSimulating: boolean;
  setSimulating: (simulating: boolean) => void;
  simulationStep: number;
  setSimulationStep: (step: number) => void;
}

export const useAppStore = create<AppState>((set) => ({
  activeView: 'overview',
  setActiveView: (view) => set({ activeView: view }),

  theme: 'dark',
  setTheme: (theme) => {
    document.documentElement.setAttribute('data-theme', theme);
    set({ theme });
  },

  isCommandPaletteOpen: false,
  setCommandPaletteOpen: (open) => set({ isCommandPaletteOpen: open }),

  isNotificationOpen: false,
  setNotificationOpen: (open) => set({ isNotificationOpen: open }),

  notifications: [
    {
      id: 'notif-1',
      timestamp: new Date().toLocaleTimeString(),
      type: 'success',
      title: 'System Boot Initialized',
      message: 'Hero City Bengaluru pre-computed baseline graph cached successfully (<50ms).',
      read: false
    },
    {
      id: 'notif-2',
      timestamp: new Date().toLocaleTimeString(),
      type: 'info',
      title: 'AI Segmentation Shaders Ready',
      message: 'SegFormer MiT-B2 wrapper initialized with 8 occlusion classes.',
      read: false
    }
  ],
  addNotification: (item) => set((state) => ({
    notifications: [
      {
        ...item,
        id: `notif-${Date.now()}-${Math.random().toString(36).substr(2, 4)}`,
        timestamp: new Date().toLocaleTimeString(),
        read: false
      },
      ...state.notifications
    ]
  })),
  markAllNotificationsRead: () => set((state) => ({
    notifications: state.notifications.map((n) => ({ ...n, read: true }))
  })),

  selectedEdgeId: null,
  setSelectedEdgeId: (id) => set({ selectedEdgeId: id }),

  selectedNodeId: null,
  setSelectedNodeId: (id) => set({ selectedNodeId: id }),

  selectedRepairId: null,
  setSelectedRepairId: (id) => set({ selectedRepairId: id }),

  isSimulating: false,
  setSimulating: (simulating) => set({ isSimulating: simulating }),
  simulationStep: 1,
  setSimulationStep: (step) => set({ simulationStep: step })
}));
