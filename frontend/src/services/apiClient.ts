const BASE_URL = 'http://localhost:8000/api/v1';

export interface SystemConfigData {
  ai_confidence_threshold: number;
  min_ai_confidence_barrier: number;
  rdp_epsilon: number;
  spur_length_threshold: number;
  criticality_weights: {
    betweenness: number;
    closeness: number;
    degree: number;
    eigenvector: number;
    kcore: number;
    articulation: number;
  };
}

export interface HealthResponseData {
  status: string;
  version: string;
  timestamp: string;
  modules_initialized: {
    gis: boolean;
    ai: boolean;
    graph: boolean;
  };
}

export const apiClient = {
  async getHealth(): Promise<HealthResponseData> {
    const res = await fetch(`${BASE_URL}/health`);
    if (!res.ok) throw new Error(`Health check failed: ${res.statusText}`);
    return res.json();
  },

  async getConfig(): Promise<SystemConfigData> {
    const res = await fetch(`${BASE_URL}/config`);
    if (!res.ok) throw new Error(`Fetch config failed: ${res.statusText}`);
    return res.json();
  },

  async updateConfig(config: SystemConfigData): Promise<SystemConfigData> {
    const res = await fetch(`${BASE_URL}/config`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config),
    });
    if (!res.ok) throw new Error(`Update config failed: ${res.statusText}`);
    return res.json();
  },

  async runAiInference(imageId: string, occlusionType: string, thresh: number): Promise<any> {
    const res = await fetch(`${BASE_URL}/ai/infer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        image_id: imageId,
        occlusion_type: occlusionType,
        confidence_threshold: thresh,
      }),
    });
    if (!res.ok) throw new Error(`AI inference failed: ${res.statusText}`);
    return res.json();
  },

  async constructGraph(): Promise<any> {
    const res = await fetch(`${BASE_URL}/graph/construct`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image_id: 'bengaluru_flood_01', rdp_epsilon: 2.0, spur_threshold: 15.0 }),
    });
    if (!res.ok) throw new Error(`Graph construction failed: ${res.statusText}`);
    return res.json();
  },

  async healGraph(searchRadius: number, maxCandidates: number): Promise<any> {
    const res = await fetch(`${BASE_URL}/graph/heal`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ search_radius_meters: searchRadius, max_candidates: maxCandidates }),
    });
    if (!res.ok) throw new Error(`Graph healing failed: ${res.statusText}`);
    return res.json();
  },

  async getBaselineGeoJson(): Promise<any> {
    const res = await fetch(`${BASE_URL}/graph/baseline`);
    if (!res.ok) throw new Error(`Fetch baseline failed: ${res.statusText}`);
    return res.json();
  },

  async getCriticality(): Promise<any> {
    const res = await fetch(`${BASE_URL}/graph/criticality`);
    if (!res.ok) throw new Error(`Fetch criticality failed: ${res.statusText}`);
    return res.json();
  },

  async runSimulation(disasterType: string, failureFraction: number): Promise<any> {
    const res = await fetch(`${BASE_URL}/simulation/disrupt`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        disaster_type: disasterType,
        bounding_box: { min_lat: 12.91, max_lat: 12.93, min_lon: 77.51, max_lon: 77.53 },
        failure_fraction: failureFraction,
      }),
    });
    if (!res.ok) throw new Error(`Simulation failed: ${res.statusText}`);
    return res.json();
  },

  async exportGeoJson(): Promise<any> {
    const res = await fetch(`${BASE_URL}/export/geojson`);
    if (!res.ok) throw new Error(`Export GeoJSON failed: ${res.statusText}`);
    return res.json();
  },
};
