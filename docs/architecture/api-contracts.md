# API Contracts

The frontend starter currently calls three endpoints. The backend implements compatible contracts:

## Health
`GET /api/v1/health`

```json
{"status":"ok","service":"yatranook-api","database":"connected"}
```

## Destination search
`GET /api/v1/destinations?search=puri&region=Odisha`

Returns a JSON array with `id`, `name`, `location`, `category`, `description`, `image`, `distanceKm`, `duration`, `priceLabel`, `tags`, latitude/longitude, and source metadata. Seed catalogue records are starter content, not verified operational visitor data.

## Trip planning
`POST /api/v1/assistant/plan`

```json
{
  "origin": "Bhubaneswar",
  "region": "Odisha",
  "budget": 1500,
  "budgetType": "total",
  "travelers": 1,
  "duration": "day",
  "interests": ["Temples", "Nature"]
}
```

Returns `mode`, `message`, `suggested`, `sources`, `budget_analysis`, and `warnings`. Without an LLM provider key it uses a deterministic fallback. It accepts valid low positive budgets rather than enforcing a fixed minimum.

## Route preview
`POST /api/v1/routes/optimize`

```json
{
  "origin": {"id":"origin","name":"Bhubaneswar","latitude":20.2961,"longitude":85.8245},
  "stops": [
    {"id":"dhauli","name":"Dhauli","latitude":20.192,"longitude":85.839},
    {"id":"lingaraj","name":"Lingaraj","latitude":20.2376,"longitude":85.8348}
  ],
  "mode":"balanced"
}
```

Without `OSRM_BASE_URL`, the response is `geographic_order_preview` and explicitly identifies straight-line distance. With a configured OSRM-compatible route provider, the response includes provider road distance, duration, and geometry for the supplied stop sequence. It is not a fare optimizer.

## Authentication and saved trips

Register with `POST /api/v1/auth/register` using `{ "email", "full_name", "password" }`. Login with `POST /api/v1/auth/login` using `{ "email", "password" }`. Use the returned bearer token with `/api/v1/auth/me` and `/api/v1/trips`.

Trip creation accepts title, origin, region, budget, budget_type, travelers, duration, interests, itinerary, and optional estimated_total. Trip operations are scoped to the authenticated owner.
