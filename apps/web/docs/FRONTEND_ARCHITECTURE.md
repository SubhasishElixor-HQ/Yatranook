# Yatranook Frontend Architecture

## Application routes

| Route | Screen | Main responsibility |
|---|---|---|
| `/` | Public landing | Product story and entry points |
| `/app/dashboard` | Overview | Current trip draft and discovery shortcuts |
| `/app/planner` | AI planner | Progressive trip requirements and assistant conversation |
| `/app/explore` | Explore Odisha | Destination search, categories, nearby filter |
| `/app/destinations/:id` | Destination detail | Destination information and planning entry point |
| `/app/itinerary` | Route & itinerary | Editable stop order, route-mode selection, map preview |
| `/app/budget` | Budget planner | Budget limit, illustrative expense breakdown, sample optimization |
| `/app/trips` | My trips | Local trip draft view |
| `/app/saved` | Saved places | Browser-persisted saved destinations |
| `/app/settings` | Settings | Profile and preference prototype |

## State ownership

- TanStack Query owns server-state caching and API request lifecycle.
- Zustand persist stores the active trip draft and saved destination IDs in browser local storage.
- Page-local React state owns temporary form values, search filters, chat transcript, and UI notices.
- Backend data must become authoritative for authenticated trips, verified destinations, route results, provider quotations, and reservation state.

## API boundary

`src/lib/api/client.ts` is the single Axios client and currently contains example contracts for:

- `GET /api/v1/health`
- `GET /api/v1/destinations?search=...`
- `POST /api/v1/assistant/plan`

These are integration placeholders. Confirm endpoint paths and payload schemas against the actual FastAPI OpenAPI document before enabling the API base URL.

## Demo-data boundaries

`src/data/demo.ts` contains example destinations, itinerary stops, and illustrative expense amounts. Do not use these as current visitor facts or real travel quotes. `RoutePreview` is a designed visual preview, not a geospatial routing result. Replace the demo adapter with real FastAPI and provider data before production use.

## Production integration sequence

1. Generate TypeScript API types from FastAPI OpenAPI.
2. Implement authenticated trip, destination, and itinerary endpoints.
3. Replace local demo records with API queries.
4. Connect geocoding and route provider adapters.
5. Make backend budget calculations authoritative.
6. Add validated booking-provider handoff and confirmation states only when the provider workflow exists.
7. Add user-account synchronization and server-side saved places.
