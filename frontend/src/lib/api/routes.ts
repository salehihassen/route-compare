import { apiClient } from './client';
import { RouteRequest, RouteResponse, HealthResponse } from '../../types/api';

export const routesApi = {
  calculate: async (data: RouteRequest): Promise<RouteResponse> => {
    const response = await apiClient.post<RouteResponse>('/routes', data);
    return response.data;
  },

  health: async (): Promise<HealthResponse> => {
    const response = await apiClient.get<HealthResponse>('/health');
    return response.data;
  },
};
