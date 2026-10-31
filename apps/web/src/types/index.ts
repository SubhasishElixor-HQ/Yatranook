export type TravelCategory = 'Temple' | 'Beach' | 'Nature' | 'Heritage' | 'Wildlife' | 'Food' | 'Culture';
export type RouteMode = 'cheapest' | 'fastest' | 'shortest' | 'balanced';

export interface Destination {
  id: string;
  name: string;
  location: string;
  category: TravelCategory;
  description: string;
  image: string;
  distanceKm?: number;
  duration?: string;
  priceLabel?: string;
  tags: string[];
}

export interface TripRequest {
  origin: string;
  region: string;
  budget: number;
  budgetType: 'total' | 'per-person';
  travelers: number;
  duration: 'day' | 'weekend' | 'multi-day';
  interests: string[];
}

export interface ItineraryStop {
  id: string;
  name: string;
  area: string;
  time: string;
  duration: string;
  travel: string;
  note: string;
  latitude?: number;
  longitude?: number;
}

export interface ApiHealth {
  status: 'ok' | 'degraded' | 'unavailable';
  mode: 'api' | 'demo';
}

export interface RouteOptimizeResult {
  status: 'provider_route' | 'geographic_order_preview';
  mode: string;
  ordered_stops: { id: string; name: string; latitude: number; longitude: number }[];
  straight_line_distance_km: number;
  road_distance_km?: number | null;
  duration_minutes?: number | null;
  route_geometry?: Record<string, unknown> | null;
  limitations: string[];
}

export interface TripPlanResult {
  mode: 'live' | 'fallback' | 'demo';
  message: string;
  suggested: Destination[];
  sources?: { title: string; source_name: string; source_url?: string | null; content?: string }[];
  warnings?: string[];
  budget_analysis?: { supplied_budget: number; effective_group_budget: number; currency: string; estimate_status: string; note: string };
}

export interface TripChatResult {
  mode: 'live' | 'fallback' | 'demo';
  message: string;
  suggested: Destination[];
  sources?: { title: string; source_name: string; source_url?: string | null; content?: string }[];
  warnings?: string[];
}
