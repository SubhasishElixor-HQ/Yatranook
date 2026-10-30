# Yatranook Frontend

A React + TypeScript frontend starter for Yatranook, an AI-assisted tourism and trip-planning product initially focused on Odisha.

## Included

- Public landing page.
- Workspace dashboard.
- Conversational travel planner UI.
- Destination discovery and destination detail pages.
- Route and itinerary editor with illustrative map visualization.
- Budget planner with low-budget-friendly input handling.
- Saved trip draft view.
- Settings and privacy preference UI.
- Typed Axios API client with an optional FastAPI base URL.
- Local demo adapter for destination search and trip request preview.
- Login and registration views backed by the API when configured; access tokens stay in memory in this starter.
- Authenticated trip-save/list wiring to the backend.
- Responsive design system and reusable components.
- Vitest, Testing Library, and Playwright setup.

## Important implementation boundary

This ZIP contains a **frontend starter with local demo interactions**. It does not include the FastAPI backend, database, LLM, RAG pipeline, geocoding, live routing, live prices, accommodation availability, or booking integrations. Sample destinations, budget amounts, stops, and route graphics are illustrative UI data, not verified travel recommendations. The UI deliberately labels these limitations.

The map graphic is an illustrative visual, not a live geospatial map. The “Open directions” action hands off to Google Maps using the sample origin/destination. Connect a real routing provider and backend itinerary data before relying on route distances or travel times.

## Requirements

- Node.js 22.12+ recommended (Vite 8 requires a current Node release).
- npm 10+

## Setup

```bash
npm install
cp .env.example .env.local
npm run dev
```

On Windows PowerShell, copy the environment file with:

```powershell
Copy-Item .env.example .env.local
```

The app opens at `http://localhost:5173`.

## Connect FastAPI

Set `VITE_API_BASE_URL` in `.env.local`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

The backend in the parent repository implements the frontend's primary contracts:

- `GET /api/v1/health`
- `GET /api/v1/destinations?search=...`
- `POST /api/v1/assistant/plan`
- `POST /api/v1/routes/optimize`
- `POST /api/v1/auth/register` and `POST /api/v1/auth/login`
- `GET /api/v1/trips` and `POST /api/v1/trips` for signed-in users

In Docker, `VITE_API_BASE_URL=/` and Nginx forwards `/api/` to FastAPI. Do not add private provider keys to `VITE_*` variables: frontend environment variables are visible to browser users.

## Quality checks

```bash
npm run typecheck
npm run test
npm run lint
npm run build
```

Run the browser smoke test after installing the Playwright browser:

```bash
npx playwright install chromium
npm run e2e
```

## Project structure

```text
src/
├── components/       # shared UI and application shell
├── data/             # clearly marked illustrative demo data
├── lib/api/          # typed API client and demo adapter
├── pages/            # route-level pages
├── store/            # persisted local trip draft state
├── test/             # test setup
├── types/            # shared TypeScript domain types
├── App.tsx
├── main.tsx
└── styles.css
```

## Next backend milestones

1. Align API contracts with FastAPI OpenAPI.
2. Implement user and trip persistence.
3. Add destination catalog and verified tourism source ingestion.
4. Add LLM orchestration and RAG retrieval.
5. Add deterministic budget calculation and geospatial route planning.
6. Integrate map, geocoding, and routing providers.
7. Add provider handoff/booking integration with verified confirmation state.
