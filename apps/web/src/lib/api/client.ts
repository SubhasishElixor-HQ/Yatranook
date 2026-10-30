import axios from 'axios';
import type { ApiHealth, Destination, RouteMode, RouteOptimizeResult, TripPlanResult, TripRequest } from '../../types';
import { destinations } from '../../data/demo';
import { useAuthStore, type SessionUser } from '../../store/useAuthStore';

const configuredBaseURL = import.meta.env.VITE_API_BASE_URL?.trim();

export const api = axios.create({
  baseURL: configuredBaseURL ? `${configuredBaseURL.replace(/\/$/, '')}/api/v1` : undefined,
  timeout: 15_000,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const apiMode = configuredBaseURL ? 'api' : 'demo';

export async function getHealth(): Promise<ApiHealth> {
  if (!configuredBaseURL) return { status: 'degraded', mode: 'demo' };
  try {
    await api.get('/health');
    return { status: 'ok', mode: 'api' };
  } catch {
    return { status: 'unavailable', mode: 'api' };
  }
}

export async function searchDestinations(query: string): Promise<Destination[]> {
  if (configuredBaseURL) {
    const { data } = await api.get<Destination[]>('/destinations', { params: { search: query } });
    return data;
  }
  const normalized = query.trim().toLowerCase();
  if (!normalized) return destinations;
  return destinations.filter((item) => `${item.name} ${item.location} ${item.category} ${item.tags.join(' ')}`.toLowerCase().includes(normalized));
}

export async function createTripPlan(input: TripRequest): Promise<TripPlanResult> {
  if (configuredBaseURL) {
    const { data } = await api.post<TripPlanResult>('/assistant/plan', input);
    return data;
  }
  return {
    mode: 'demo' as const,
    message: `I have your starting point as ${input.origin}, your region as ${input.region || 'flexible'}, and your budget as ₹${input.budget.toLocaleString('en-IN')} ${input.budgetType === 'total' ? 'for the trip' : 'per person'}. A small positive budget is valid. I would compare nearby options first, then build a route that balances distance, time, and cost. This preview uses sample catalogue data; connect FastAPI and verified routing/fare providers for live results.`,
    suggested: destinations.filter((d) => ['Temple', 'Heritage', 'Nature'].includes(d.category)).slice(0, 3),
  };
}

export async function registerAccount(input: { email: string; full_name: string; password: string }): Promise<SessionUser> {
  const { data } = await api.post<SessionUser>('/auth/register', input);
  return data;
}

export async function loginAccount(input: { email: string; password: string }): Promise<{ access_token: string }> {
  const { data } = await api.post<{ access_token: string }>('/auth/login', input);
  return data;
}

export async function getCurrentUser(): Promise<SessionUser> {
  const { data } = await api.get<SessionUser>('/auth/me');
  return data;
}

export interface SavedTrip {
  id: string;
  title: string;
  origin: string;
  region: string;
  budget: string;
  budget_type: 'total' | 'per-person';
  travelers: number;
  duration: 'day' | 'weekend' | 'multi-day';
  interests: string[];
  itinerary: Record<string, unknown>;
  estimated_total: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export async function listSavedTrips(): Promise<SavedTrip[]> {
  const { data } = await api.get<SavedTrip[]>('/trips');
  return data;
}

export async function saveTrip(input: TripRequest): Promise<SavedTrip> {
  const { data } = await api.post<SavedTrip>('/trips', {
    title: `${input.region || 'Odisha'} trip plan`,
    origin: input.origin,
    region: input.region,
    budget: input.budget,
    budget_type: input.budgetType,
    travelers: input.travelers,
    duration: input.duration,
    interests: input.interests,
    itinerary: { status: 'planning_draft', note: 'Save the generated itinerary here when planning is connected.' },
  });
  return data;
}

export async function optimizeRoute(input: {
  origin: { id: string; name: string; latitude: number; longitude: number };
  stops: { id: string; name: string; latitude: number; longitude: number }[];
  mode: RouteMode;
}): Promise<RouteOptimizeResult> {
  const { data } = await api.post<RouteOptimizeResult>('/routes/optimize', input);
  return data;
}
