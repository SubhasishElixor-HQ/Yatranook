import { create } from 'zustand';

export interface SessionUser {
  id: string;
  email: string;
  full_name: string;
  created_at: string;
}

interface AuthState {
  accessToken: string | null;
  user: SessionUser | null;
  setAccessToken: (token: string) => void;
  setSession: (token: string, user: SessionUser) => void;
  clearSession: () => void;
}

// Access tokens intentionally remain in memory in this starter. A full public launch
// should add a secure HttpOnly-cookie session or a carefully designed refresh flow.
export const useAuthStore = create<AuthState>((set) => ({
  accessToken: null,
  user: null,
  setAccessToken: (accessToken) => set({ accessToken }),
  setSession: (accessToken, user) => set({ accessToken, user }),
  clearSession: () => set({ accessToken: null, user: null }),
}));
