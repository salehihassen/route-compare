export interface RouteRequest {
  origin: string;
  destination: string;
  departure_time?: string;
  arrival_time?: string;
}

export interface RouteResponse {
  success: boolean;
  time_field?: string;
  time_value?: string;
  routes: Route[];
  api_metadata: {
    timestamp: string;
    routes_count: number;
    request_params: {
      origin: string;
      destination: string;
      has_departure_time: boolean;
      has_arrival_time: boolean;
    };
  };
  error?: string;
}

export interface Route {
  localizedValues: {
    distance: { text: string };
    duration: { text: string };
    staticDuration: { text: string };
  };
  duration: string; // e.g. "1800s"
  distanceMeters: number;
  staticDuration: string;
  polyline: {
    encodedPolyline: string;
  };
  description?: string;
  warnings?: string[];
  viewport?: {
    low: { latitude: number; longitude: number };
    high: { latitude: number; longitude: number };
  };
  travelAdvisory?: {
    speedReadingIntervals?: {
      startPolylinePointIndex: number;
      endPolylinePointIndex: number;
      speed: string;
    }[];
  };
  legs: Leg[];
}

export interface Leg {
  distanceMeters: number;
  duration: string;
  staticDuration: string;
  startLocation: Location;
  endLocation: Location;
  steps: Step[];
}

export interface Step {
  distanceMeters: number;
  staticDuration: string;
  polyline: {
    encodedPolyline: string;
  };
  startLocation: Location;
  endLocation: Location;
  navigationInstruction?: {
    maneuver: string;
    instructions: string;
  };
}

export interface Location {
  latLng: {
    latitude: number;
    longitude: number;
  };
}

export interface HealthResponse {
  status: string;
  service: string;
  timestamp: string;
  api_key_configured: boolean;
}
