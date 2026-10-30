# Yatranook Feature Roadmap

This roadmap turns the proposed product into implementation-sized milestones. Priorities: **P0** is required for the MVP, **P1** follows once the core workflow is evaluated, and **P2** is future scope. A feature is complete only when its acceptance criteria are demonstrated.

## MVP feature sequence

| Order | Feature | Priority | Dependencies | Acceptance criteria |
|---|---|---|---|---|
| 0 | Project foundation | P0 | Pilot region and stack decision | Web and API app bootstraps, environment configuration, database connection, OpenAPI contract, CI checks and documented local setup exist; no secrets are committed |
| 1 | Curated destination data | P0 | Source policy and reviewer | Initial pilot records have stable IDs, names/aliases, region/categories, descriptions, source URLs, review status and last-verified dates; import validates records and can be repeated safely |
| 2 | Destination discovery | P0 | Curated destination data | Traveler can search by text, district/region and supported interests; result/detail views show evidence and freshness; empty and invalid searches return clear states |
| 3 | Evidence retrieval | P0 | Approved source records and chunks | A query returns ranked passages linked to parent source and freshness metadata; test questions can be reviewed against expected supporting sources |
| 4 | Tourism Q&A | P0 | Evidence retrieval; model adapter decision | Response includes source references; insufficient/stale/conflicting evidence yields clarification or uncertainty; output may only cite retrieved evidence IDs |
| 5 | Trip request and clarification | P0 | API contracts and UI shell | Request accepts origin, destination scope, dates or duration, budget/currency, interests and pace; asks for material missing inputs rather than silently guessing |
| 6 | Itinerary draft | P0 | Destination discovery, trip request | Produces an editable, day-wise recommendation with candidate reasons, visit-duration assumptions, evidence links, cost categories and unknowns |
| 7 | Deterministic feasibility checks | P0 | Itinerary draft and budget model | Time totals, budget arithmetic, overlap and known access checks are computed by code; `pass`, `warning`, `fail` and `unknown` states are distinguishable |
| 8 | Itinerary revision | P0 | Draft and validator | Changing a stop, duration or budget recomputes affected results and preserves other constraints; changes are shown to the traveler |
| 9 | Pilot evaluation | P0 | All prior MVP features | Predeclared answer/citation, retrieval, constraint, usability and failure criteria are evaluated; dated report documents sample, method and limitations |
| 10 | Production baseline | P0 for public pilot | Evaluated MVP | Secrets, rate limits, redacted logs, monitoring, backups, demonstrated restore, migration/rollback process and runbooks are in place |

## Later features

| Feature | Priority | Add when |
|---|---|---|
| Maps and route estimates | P1 | A provider's regional coverage, terms, attribution, costs and failure behavior are verified |
| Weather forecasts | P1 | A suitable provider and forecast-use policy are verified; the UI can show forecast period and retrieval time |
| Odia and Hindi support | P1 | Human review, place-name handling and language-specific evaluation are available |
| Saved itineraries/accounts | P1 | Research supports persistence and ownership, retention, deletion and authorization are designed |
| Admin content review UI | P1 | Manual curation becomes a bottleneck and reviewers need role-based workflow |
| Accessibility-aware planning | P2 | Reliable accessibility data and user research support recommendations that can be maintained |
| Voice, collaboration, alerts, bookings/payments | P2 | Separate product, provider, privacy, security and operational approvals are complete |

## First implementation milestone: foundation + destination discovery

Start with this sequence:

1. Confirm one pilot region and define a source allowlist and review owner.
2. Bootstrap `apps/web` and `apps/api`; document local development and configuration.
3. Define the destination and source schema with migrations.
4. Prepare and validate a small, reviewed seed dataset.
5. Implement destination list/detail APIs and the shared OpenAPI contract.
6. Build search/filter and destination detail screens with source/freshness labels.
7. Review the flow with target travelers and correct confusing or missing data before adding generative AI.

### First milestone exit gate

The first milestone is complete when a fresh local setup can load the reviewed dataset, search and display destination details, preserve provenance in API responses, and show clear empty/error states. This gate does not claim that the assistant or itinerary planner is implemented.

## Feature completion checklist

- Requirement and acceptance criteria are recorded.
- API request/response contract is defined and versioned.
- Empty, invalid, stale, unavailable and error states are handled.
- Source provenance and freshness are preserved wherever factual travel content is shown.
- Deterministic logic is used for arithmetic, known constraints and provider status.
- Required automated and human evaluation evidence is recorded before claiming quality.
- Privacy, retention and deployment impact are reviewed before storing personal trip data or enabling a provider.
