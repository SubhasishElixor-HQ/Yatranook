import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppShell } from './components/AppShell';
import { LandingPage } from './pages/LandingPage';
import { DashboardPage } from './pages/DashboardPage';
import { PlannerPage } from './pages/PlannerPage';
import { ExplorePage } from './pages/ExplorePage';
import { ItineraryPage } from './pages/ItineraryPage';
import { BudgetPage } from './pages/BudgetPage';
import { TripsPage } from './pages/TripsPage';
import { SettingsPage } from './pages/SettingsPage';
import { SavedPlacesPage } from './pages/SavedPlacesPage';
import { DestinationPage } from './pages/DestinationPage';
import { AuthPage } from './pages/AuthPage';

const queryClient = new QueryClient({ defaultOptions: { queries: { staleTime: 30_000, retry: 1, refetchOnWindowFocus: false } } });

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage/>}/>
          <Route path="/login" element={<AuthPage mode="login"/>}/>
          <Route path="/register" element={<AuthPage mode="register"/>}/>
          <Route path="/app" element={<AppShell/>}>
            <Route index element={<Navigate to="dashboard" replace/>}/>
            <Route path="dashboard" element={<DashboardPage/>}/>
            <Route path="planner" element={<PlannerPage/>}/>
            <Route path="explore" element={<ExplorePage/>}/>
            <Route path="destinations/:id" element={<DestinationPage/>}/>
            <Route path="itinerary" element={<ItineraryPage/>}/>
            <Route path="budget" element={<BudgetPage/>}/>
            <Route path="trips" element={<TripsPage/>}/><Route path="saved" element={<SavedPlacesPage/>}/>
            <Route path="settings" element={<SettingsPage/>}/>
          </Route>
          <Route path="*" element={<Navigate to="/" replace/>}/>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
