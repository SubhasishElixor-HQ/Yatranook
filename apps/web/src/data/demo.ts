import type { Destination, ItineraryStop } from '../types';

export const destinations: Destination[] = [
  {
    id: 'konark', name: 'Konark Sun Temple', location: 'Konark, Odisha', category: 'Heritage',
    description: 'Explore the remarkable stone architecture and history of the Sun Temple.',
    image: 'https://images.unsplash.com/photo-1606293926075-69a00dbfde81?auto=format&fit=crop&w=1000&q=85',
    distanceKm: 65, duration: '1.5–2 hours', priceLabel: 'Check current visitor fees', tags: ['Architecture', 'History', 'UNESCO']
  },
  {
    id: 'puri-beach', name: 'Puri Beach', location: 'Puri, Odisha', category: 'Beach',
    description: 'A lively coastline for a relaxed walk, sea views, and local food experiences.',
    image: 'https://images.unsplash.com/photo-1519046904884-53103b34b206?auto=format&fit=crop&w=1000&q=85',
    distanceKm: 60, duration: '1–2 hours', priceLabel: 'Public beach access; verify local activities', tags: ['Coastline', 'Sunrise', 'Food']
  },
  {
    id: 'chilika', name: 'Chilika Lake', location: 'Satapada, Odisha', category: 'Nature',
    description: 'Discover a vast coastal lagoon known for birdlife and changing landscapes.',
    image: 'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1000&q=85',
    distanceKm: 105, duration: 'Half day', priceLabel: 'Boat and activity costs vary', tags: ['Lake', 'Birdlife', 'Nature']
  },
  {
    id: 'lingaraj', name: 'Lingaraj Temple', location: 'Bhubaneswar, Odisha', category: 'Temple',
    description: 'A significant temple complex showcasing Kalinga-style architecture.',
    image: 'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=1000&q=85',
    distanceKm: 4, duration: '45–90 minutes', priceLabel: 'Check visitor access rules', tags: ['Temple', 'Architecture', 'Culture']
  },
  {
    id: 'dhauli', name: 'Dhauli Shanti Stupa', location: 'Dhauli, Bhubaneswar', category: 'Heritage',
    description: 'A peaceful hilltop landmark associated with the history of Ashoka and Kalinga.',
    image: 'https://images.unsplash.com/photo-1590050752117-23a9d709bb31?auto=format&fit=crop&w=1000&q=85',
    distanceKm: 8, duration: '45–60 minutes', priceLabel: 'Verify current access details', tags: ['History', 'Peace', 'Viewpoint']
  },
  {
    id: 'nandankanan', name: 'Nandankanan', location: 'Bhubaneswar, Odisha', category: 'Wildlife',
    description: 'A nature and wildlife destination with a range of visitor experiences.',
    image: 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1000&q=85',
    distanceKm: 18, duration: '3–4 hours', priceLabel: 'Entry and safari fees vary', tags: ['Wildlife', 'Family', 'Nature']
  }
];

export const demoStops: ItineraryStop[] = [
  { id: 'stop-1', name: 'Lingaraj Temple area', area: 'Old Town, Bhubaneswar', time: '08:00 AM', duration: '60 min', travel: 'Starting point', note: 'Begin with the heritage quarter. Check visitor access and local rules before arrival.', latitude: 20.2376, longitude: 85.8348 },
  { id: 'stop-2', name: 'Dhauli Shanti Stupa', area: 'Dhauli', time: '10:00 AM', duration: '45 min', travel: 'Approx. 8 km · route data needed', note: 'Allow time for the hilltop viewpoint and peaceful surroundings.', latitude: 20.1920, longitude: 85.8390 },
  { id: 'stop-3', name: 'Local lunch stop', area: 'Bhubaneswar', time: '12:00 PM', duration: '60 min', travel: 'Route to be confirmed', note: 'Choose an affordable local restaurant based on current availability.', latitude: 20.2500, longitude: 85.8400 },
  { id: 'stop-4', name: 'Ekamra heritage walk', area: 'Bhubaneswar', time: '02:00 PM', duration: '90 min', travel: 'Nearby area · walking where suitable', note: 'Finish with a relaxed cultural walk before returning.', latitude: 20.2630, longitude: 85.8330 }
];

export const demoBudget = [
  { label: 'Local transport', amount: 500, color: 'blue' },
  { label: 'Food & refreshments', amount: 450, color: 'teal' },
  { label: 'Entry & activities', amount: 250, color: 'amber' },
  { label: 'Buffer', amount: 200, color: 'slate' }
];
