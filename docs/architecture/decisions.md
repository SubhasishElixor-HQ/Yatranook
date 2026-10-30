# Initial Architecture Decisions

## ADR-001 — Modular monolith

**Decision:** Keep the API in one FastAPI deployment with distinct service modules.

**Reason:** Early product scope and small-team operations do not justify microservices yet. Domain boundaries remain explicit for future extraction.

## ADR-002 — PostgreSQL as system of record

**Decision:** Store user, destination, trip, and source records in PostgreSQL; use pgvector for optional semantic retrieval.

**Reason:** Relational consistency, mature tooling, transactional updates, and extension support reduce infrastructure complexity.

## ADR-003 — LLM is not the authority for calculations or state

**Decision:** Use LLMs for language understanding and explanation; deterministic services own arithmetic, validations, permissions, and transaction state.

**Reason:** Budget calculations and consequential state transitions must be testable and repeatable.

## ADR-004 — Route provider is optional and explicit

**Decision:** Without a configured routing provider, return only a labelled geographic-order preview.

**Reason:** Straight-line distance is not road distance and should never be shown as driving directions.

## ADR-005 — Provider handoff before unsupported booking automation

**Decision:** Keep booking as an external handoff until a provider contract and API integration are implemented and tested.

**Reason:** A frontend success state is not proof of a real booking or payment.
