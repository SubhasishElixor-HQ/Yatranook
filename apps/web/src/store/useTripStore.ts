import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { RouteMode, TripRequest } from '../types';

interface TripState {
  request: TripRequest;
  routeMode: RouteMode;
  savedTrip: boolean;
  savedDestinationIds: string[];
  toggleSavedDestination: (id: string) => void;
  setRequest: (partial: Partial<TripRequest>) => void;
  setRouteMode: (mode: RouteMode) => void;
  setSavedTrip: (saved: boolean) => void;
}

const initialRequest: TripRequest = {
  origin: '', region: 'Odisha', budget: 2000, budgetType: 'total', travelers: 1, duration: 'day', interests: ['Temples', 'Nature']
};

export const useTripStore = create<TripState>()(persist((set) => ({
  request: initialRequest,
  routeMode: 'balanced',
  savedTrip: false,
  savedDestinationIds: [],
  toggleSavedDestination: (id) => set((state) => ({ savedDestinationIds: state.savedDestinationIds.includes(id) ? state.savedDestinationIds.filter((savedId) => savedId !== id) : [...state.savedDestinationIds, id] })),
  setRequest: (partial) => set((state) => ({ request: { ...state.request, ...partial } })),
  setRouteMode: (routeMode) => set({ routeMode }),
  setSavedTrip: (savedTrip) => set({ savedTrip }),
}), { name: 'yatranook-trip-draft' }));
