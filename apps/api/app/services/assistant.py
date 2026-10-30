import logging

import httpx
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.destination import Destination
from app.schemas.assistant import TripPlanRequest
from app.schemas.destination import DestinationOut
from app.services.rag import retrieve_tourism_context

logger = logging.getLogger(__name__)


async def _generate_llm_message(request: TripPlanRequest, context: list[dict], suggested: list[Destination]) -> str | None:
    api_key = settings.openai_api_key.get_secret_value() if settings.openai_api_key else None
    if not api_key:
        return None
    context_text = "\n\n".join(
        f"Source: {item['source_name']} | Title: {item['title']} | URL: {item.get('source_url') or 'not supplied'}\n{item['content']}"
        for item in context
    ) or "No tourism documents matched this request. Do not invent destination facts."
    destination_text = "\n".join(f"- {item.name}: {item.description}" for item in suggested)
    system_prompt = (
        "You are Yatranook, a careful travel-planning assistant initially focused on Odisha, India. "
        "Use only supplied destination and retrieved context for factual claims. Ask for missing critical details. "
        "Never invent live prices, opening hours, route durations, availability, or booking confirmations. "
        "Distinguish estimates from verified facts. A valid low budget is not invalid; suggest practical alternatives. "
        "Do not claim to have booked anything. Reply in clear, concise English."
    )
    user_prompt = f"""Traveler request:
Origin: {request.origin}
Region preference: {request.region or 'Flexible'}
Budget: INR {request.budget} ({request.budgetType})
Travelers: {request.travelers}
Duration: {request.duration}
Interests: {', '.join(request.interests) or 'Open to suggestions'}

Available destination records:
{destination_text or 'No destination records found.'}

Retrieved tourism context:
{context_text}

Explain suitable next steps and limitations. Do not claim that exact expenses or routes are verified."""
    url = f"{settings.openai_base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": settings.openai_chat_model,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    try:
        async with httpx.AsyncClient(timeout=35.0) as client:
            response = await client.post(url, json=payload, headers={"Authorization": f"Bearer {api_key}"})
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
    except (httpx.HTTPError, KeyError, IndexError, TypeError):
        logger.exception("LLM provider call failed; using deterministic fallback response")
        return None


async def plan_trip(db: Session, request: TripPlanRequest) -> dict:
    query_terms = [term.strip() for term in request.interests if term.strip()]
    statement = select(Destination)
    if request.region:
        region_pattern = f"%{request.region}%"
        statement = statement.where(
            or_(Destination.region.ilike(region_pattern), Destination.location.ilike(region_pattern), Destination.name.ilike(region_pattern))
        )
    destinations = list(db.scalars(statement.order_by(Destination.name).limit(60)).all())
    if query_terms:
        aliases = {
            "temples": "temple", "beaches": "beach", "historical places": "heritage",
            "local food": "food", "cultural experiences": "culture", "photography": "viewpoint",
        }
        normalized = [aliases.get(term.lower(), term.lower().rstrip("s")) for term in query_terms]
        matched = [
            item for item in destinations
            if any(
                term in item.category.lower()
                or term in item.description.lower()
                or any(term in tag.lower() for tag in (item.tags or []))
                for term in normalized
            )
        ]
        if matched:
            destinations = matched
    suggested = destinations[:6]
    context = await retrieve_tourism_context(
        db,
        " ".join([request.origin, request.region, *request.interests, "tourism travel attractions"]),
    )
    message = await _generate_llm_message(request, context, suggested)
    mode = "live" if message else "fallback"
    if not message:
        effective_budget = request.budget * request.travelers if request.budgetType == "per-person" else request.budget
        available_names = ", ".join(item.name for item in suggested[:4]) or "No matching destination records are currently available"
        message = (
            f"I have your starting point as {request.origin} and your preferred region as "
            f"{request.region or 'flexible'}. Your budget is ₹{request.budget:,.0f} "
            f"({'per person' if request.budgetType == 'per-person' else 'for the whole trip'}). "
            f"That is a valid budget, so I will not reject it because it is small. "
            f"Destinations matching the available catalog include: {available_names}. "
            "The catalog is an initial seed dataset. Exact road routes, live fares, attraction fees, "
            "and opening hours are not verified by this fallback response. Connect an LLM, verified "
            "tourism sources, and routing/fare providers for a complete costed itinerary."
        )
    effective_budget = request.budget * request.travelers if request.budgetType == "per-person" else request.budget
    warnings = ["Travel costs and route durations are not calculated from live provider data."]
    if not context:
        warnings.append("No matching curated tourism documents were retrieved; destination suggestions come from the catalog only.")
    return {
        "mode": mode,
        "message": message,
        "suggested": [DestinationOut.from_model(item).model_dump(by_alias=True) for item in suggested],
        "sources": context,
        "budget_analysis": {
            "supplied_budget": request.budget,
            "effective_group_budget": effective_budget,
            "currency": "INR",
            "estimate_status": "insufficient_cost_data",
            "note": "A valid low budget is accepted. A reliable total estimate requires current transport, entry, food, and accommodation cost data.",
        },
        "warnings": warnings,
    }
