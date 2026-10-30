# Yatranook Architecture Overview

## Architectural style

Start with a **modular monolith**: one FastAPI deployment with distinct API, schema, service, model, AI/RAG, and integration modules. PostgreSQL remains the source of truth. This avoids the operational cost of microservices while preserving boundaries that can be extracted later if scale and team ownership justify it.

## Request flow

1. React captures user intent and trip context.
2. A typed client calls a versioned FastAPI endpoint.
3. Pydantic validates the payload.
4. A domain service queries PostgreSQL and the tourism knowledge store.
5. Optional LLM generation receives relevant, untrusted tourism context and must identify uncertainty.
6. Deterministic services own numeric calculations, ownership checks, and state transitions.
7. The API returns a typed response with source metadata and warnings.

## Trust boundaries

- Browser input is untrusted.
- Retrieved tourism documents are untrusted content, not system instructions.
- Provider data can be incomplete or stale.
- Booking and payment execution must occur through a real authorized provider flow and require explicit user confirmation.
- The application must not mark a booking successful without a verified provider result.

## Main modules

- `destinations`: destination catalog and public search.
- `assistant`: request-level orchestration and user-facing planning response.
- `rag`: keyword/semantic tourism context retrieval and document ingestion.
- `routing`: geographic stop ordering preview and optional OSRM route provider.
- `trips`: authenticated, user-owned saved trip records.
- `auth`: registration, login, signed access tokens, and current-user resolution.

## Current boundaries

The seed destination data is illustrative and has not been field-verified. The fallback assistant is deterministic. LLM responses depend on provider configuration. The route service explicitly labels straight-line distance as a preview unless a routing provider returns road distance and duration. No booking integration is implemented.
