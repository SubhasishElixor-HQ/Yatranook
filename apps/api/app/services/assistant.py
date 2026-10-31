import logging
import re

import httpx
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.destination import Destination
from app.schemas.assistant import TripChatRequest, TripPlanRequest
from app.schemas.destination import DestinationOut
from app.services.rag import retrieve_tourism_context

logger = logging.getLogger(__name__)


def _clean_model_response(content: str) -> str:
    cleaned = content.strip()
    if "<think>" in cleaned:
        cleaned = cleaned.split("<think>", 1)[0].strip()
    if "</think>" in cleaned:
        cleaned = cleaned.split("</think>", 1)[-1].strip()
    return cleaned


def _select_chat_destinations(
    destinations: list[Destination], request: TripChatRequest
) -> list[Destination]:
    focus = f"{request.message} {' '.join(request.interests)}".lower()
    aliases = {
        "temple": ("temple",),
        "beach": ("beach", "coast"),
        "nature": ("nature", "lake", "bird"),
        "heritage": ("heritage", "history", "architecture"),
        "wildlife": ("wildlife", "zoo", "safari"),
        "food": ("food",),
        "culture": ("culture", "heritage", "temple"),
    }
    terms = {term for keyword, values in aliases.items() if keyword in focus for term in values}
    if not terms:
        return destinations[:6]
    matches = [
        item
        for item in destinations
        if any(
            term in item.category.lower()
            or term in item.description.lower()
            or any(term in tag.lower() for tag in (item.tags or []))
            for term in terms
        )
    ]
    return (matches or destinations)[:6]


def _needs_grounded_fallback(
    message: str,
    request: TripChatRequest,
    suggested: list[Destination],
) -> bool:
    lowered = request.message.lower()

    asks_live_data = any(
        term in lowered
        for term in ("exact", "current", "today", "tomorrow", "fare", "price", "how long")
    )

    if asks_live_data and re.search(r"\d", message):
        return True

    asks_itinerary = any(
        term in lowered for term in ("order", "route", "itinerary", "visit first", "places should")
    )

    unsupported_itinerary_claims = (
        "expensive",
        "cheapest",
        "nearest",
        "nearby",
        "distance",
        " km",
        "minutes",
        "hours",
        "fee",
        "reducing unnecessary travel",
        "minimiz",
        "save time",
    )

    if not asks_itinerary:
        return False

    local_names = [
        item.name.lower()
        for item in suggested
        if request.origin and request.origin.lower() in item.location.lower()
    ]

    other_names = [item.name.lower() for item in suggested if item.name.lower() not in local_names]

    local_position = min(
        (message.lower().find(name) for name in local_names if name in message.lower()),
        default=-1,
    )

    other_position = min(
        (message.lower().find(name) for name in other_names if name in message.lower()),
        default=-1,
    )

    return (
        len(message) < 80
        or any(term in message.lower() for term in unsupported_itinerary_claims)
        or (local_position == -1 and bool(local_names))
        or (other_position >= 0 and local_position > other_position)
    )


def _needs_plan_fallback(message: str) -> bool:
    lowered = message.lower()

    unsupported_budget_claims = (
        "not sufficient",
        "does not seem sufficient",
        "recommended minimum",
        "too low",
        "too high",
        "minimum budget",
        "not enough budget",
    )

    return any(term in lowered for term in unsupported_budget_claims)


async def _generate_llm_message(
    request: TripPlanRequest, context: list[dict], suggested: list[Destination]
) -> str | None:
    context_text = (
        "\n\n".join(
            f"Source: {item['source_name']} | Title: {item['title']} | URL: {item.get('source_url') or 'not supplied'}\n{item['content']}"
            for item in context
        )
        or "No tourism documents matched this request. Do not invent destination facts."
    )
    destination_text = "\n".join(f"- {item.name}: {item.description}" for item in suggested)
    system_prompt = (
        "You are Yatranook, a careful travel-planning assistant initially focused on Odisha, India. "
        "Use only the supplied destination records and retrieved context for factual claims. You may mention only "
        "destination names present in those supplied records; never add remembered places. Ask for missing critical details. "
        "Never invent live prices, opening hours, route durations, availability, or booking confirmations. "
        "Distinguish estimates from verified facts. Treat every positive budget as valid and suggest practical "
        "alternatives without judging it as too low or too high. "
        "Do not claim to have booked anything. If a user asks for an exact current price or travel time and no "
        "provider data is supplied, say it is unavailable and do not provide a guessed number. "
        "Output only the final answer in clear, concise English. Never output analysis, deliberation, or a reasoning trace."
    )
    user_prompt = f"""Traveler request:
Origin: {request.origin}
Region preference: {request.region or "Flexible"}
Budget: INR {request.budget} ({request.budgetType})
Travelers: {request.travelers}
Duration: {request.duration}
Interests: {", ".join(request.interests) or "Open to suggestions"}

Available destination records:
{destination_text or "No destination records found."}

Retrieved tourism context:
{context_text}

Explain suitable next steps and limitations. Use only the listed destination records. Do not mention any other place,
and do not claim that exact expenses or routes are verified."""
    url = f"{settings.ollama_base_url.rstrip('/')}/api/chat"
    payload = {
        "model": settings.ollama_chat_model,
        "temperature": 0.2,
        "stream": False,
        "think": False,
        "options": {"num_predict": 350},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return _clean_model_response(response.json()["message"]["content"])
    except (httpx.HTTPError, KeyError, TypeError, AttributeError):
        logger.exception("Ollama chat provider call failed; using deterministic fallback response")
        return None


async def plan_trip(db: Session, request: TripPlanRequest) -> dict:
    query_terms = [term.strip() for term in request.interests if term.strip()]
    statement = select(Destination)
    if request.region:
        region_pattern = f"%{request.region}%"
        statement = statement.where(
            or_(
                Destination.region.ilike(region_pattern),
                Destination.location.ilike(region_pattern),
                Destination.name.ilike(region_pattern),
            )
        )
    destinations = list(db.scalars(statement.order_by(Destination.name).limit(60)).all())
    if query_terms:
        aliases = {
            "temples": "temple",
            "beaches": "beach",
            "historical places": "heritage",
            "local food": "food",
            "cultural experiences": "culture",
            "photography": "viewpoint",
        }
        normalized = [aliases.get(term.lower(), term.lower().rstrip("s")) for term in query_terms]
        matched = [
            item
            for item in destinations
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
        " ".join(
            [request.origin, request.region, *request.interests, "tourism travel attractions"]
        ),
    )
    message = await _generate_llm_message(request, context, suggested)
    mode = "live" if message else "fallback"
    if message and _needs_plan_fallback(message):
        logger.warning(
            "Ollama planner response judged the budget without cost evidence; using deterministic response"
        )
        message = None
        mode = "fallback"
    if not message:
        effective_budget = (
            request.budget * request.travelers
            if request.budgetType == "per-person"
            else request.budget
        )
        available_names = (
            ", ".join(item.name for item in suggested[:4])
            or "No matching destination records are currently available"
        )
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
    effective_budget = (
        request.budget * request.travelers if request.budgetType == "per-person" else request.budget
    )
    warnings = ["Travel costs and route durations are not calculated from live provider data."]
    if not context:
        warnings.append(
            "No matching curated tourism documents were retrieved; destination suggestions come from the catalog only."
        )
    return {
        "mode": mode,
        "message": message,
        "suggested": [
            DestinationOut.from_model(item).model_dump(by_alias=True) for item in suggested
        ],
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


async def _generate_chat_message(
    request: TripChatRequest,
    context: list[dict],
    suggested: list[Destination],
) -> str | None:
    context_text = (
        "\n\n".join(
            f"Source: {item['source_name']} | Title: {item['title']} | URL: {item.get('source_url') or 'not supplied'}\n{item['content']}"
            for item in context
        )
        or "No tourism documents matched this request. Do not invent destination facts."
    )
    destination_text = "\n".join(f"- {item.name}: {item.description}" for item in suggested)
    history_text = "\n".join(f"{item.role}: {item.content}" for item in request.history[-10:])
    system_prompt = (
        "You are Yatranook, a grounded travel-planning assistant for Odisha and India. "
        "Understand natural-language travel requests, identify useful places, and suggest an efficient "
        "order that can reduce unnecessary travel. Use only the supplied destination records and retrieved "
        "context for factual claims. Never invent live fares, opening hours, route durations, availability, "
        "or bookings. Clearly label estimates and say when a routing or fare provider is required. "
        "Ask one concise follow-up question when a critical detail is missing. If exact live prices or times are "
        "requested without provider data, say they are unavailable and do not guess. Use only facts in the supplied "
        "records; do not add remembered distances, fees, or opening hours. Output only the final answer, never analysis."
    )
    user_prompt = f"""Current trip context:
Origin: {request.origin or "not supplied"}
Region: {request.region or "flexible"}
Budget: {f"INR {request.budget} ({request.budgetType})" if request.budget else "not supplied"}
Travelers: {request.travelers}
Duration: {request.duration}
Interests: {", ".join(request.interests) or "open to suggestions"}

Conversation:
{history_text or "No previous messages."}

Traveler message:
{request.message}

Available destination records:
{destination_text or "No destination records found."}

Retrieved tourism context:
{context_text}

Give a practical answer using the selected destination records. If asked for an order, mention the selected place
names and explain that the order is a planning suggestion, not a live road-optimized route. Do not claim it reduces
actual distance or time without routing data. If asked to reduce cost,
prioritize nearby stops, fewer transfers, public/shared transport, and free or low-fee experiences, but do not claim
a precise saving without current fare data."""
    url = f"{settings.ollama_base_url.rstrip('/')}/api/chat"
    payload = {
        "model": settings.ollama_chat_model,
        "temperature": 0.2,
        "stream": False,
        "think": False,
        "options": {"num_predict": 350},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return _clean_model_response(response.json()["message"]["content"])
    except (httpx.HTTPError, KeyError, IndexError, TypeError, AttributeError):
        logger.exception("Ollama chat provider call failed; using deterministic fallback response")
        return None


async def chat_trip(db: Session, request: TripChatRequest) -> dict:
    query = " ".join(
        [
            request.message,
            request.origin,
            request.region,
            *request.interests,
            "tourism travel attractions",
        ]
    ).strip()
    context = await retrieve_tourism_context(db, query)
    statement = select(Destination)
    if request.region:
        region_pattern = f"%{request.region}%"
        statement = statement.where(
            or_(
                Destination.region.ilike(region_pattern),
                Destination.location.ilike(region_pattern),
                Destination.name.ilike(region_pattern),
            )
        )
    destinations = list(db.scalars(statement.order_by(Destination.name).limit(60)).all())
    suggested = _select_chat_destinations(destinations, request)
    message = await _generate_chat_message(request, context, suggested)
    mode = "live" if message else "fallback"
    if message and _needs_grounded_fallback(message, request, suggested):
        logger.warning(
            "Ollama response did not meet grounded output checks; using deterministic response"
        )
        message = None
        mode = "fallback"
    if not message:
        names = ", ".join(item.name for item in suggested[:4])
        asks_live_data = any(
            term in request.message.lower()
            for term in ("exact", "current", "today", "tomorrow", "fare", "price", "how long")
        )
        is_itinerary = any(
            term in request.message.lower()
            for term in ("order", "route", "itinerary", "visit first", "places should")
        )
        if asks_live_data:
            message = (
                "I cannot verify an exact current fare or travel time because no live transport provider is "
                "configured. Check a current taxi or ride-service quote before travelling; the catalogue suggestions "
                "below are not a fare estimate."
            )
        elif is_itinerary and suggested:
            ordered = sorted(
                suggested,
                key=lambda item: 0 if request.origin.lower() in item.location.lower() else 1,
            )
            ordered_names = " → ".join(item.name for item in ordered[:4])
            message = (
                f"Based on the catalogue, a practical planning order is: {ordered_names}. "
                "This is a suggested stop order, not a live road-optimized route. Keep stops in the same area "
                "where possible, and verify current transport, access rules, opening hours, and fees before travel."
            )
        else:
            message = (
                f"I can help plan that. Based on the available catalogue, consider "
                f"{names or 'nearby places in the selected region'}."
            )
        budget_note = (
            f" For your ₹{request.budget:,.0f} "
            f"{'per-person' if request.budgetType == 'per-person' else 'total'} budget, start with the closest "
            "places and group stops in the same area."
            if request.budget
            else ""
        )
        if not is_itinerary:
            message += (
                f"{budget_note} To reduce cost, use one area per day, avoid backtracking, and compare public or shared "
                "transport. I can suggest an exact stop order once you share your starting place and destination area. "
                "Live fares, road times, entry fees, and availability are not verified in this response."
            )
    warnings = [
        "Live fares and road routes require configured providers; cost-saving advice is guidance, not a quote."
    ]
    if not context:
        warnings.append(
            "No curated tourism document matched this message; suggestions come from the destination catalogue."
        )
    return {
        "mode": mode,
        "message": message,
        "suggested": [
            DestinationOut.from_model(item).model_dump(by_alias=True) for item in suggested
        ],
        "sources": context,
        "warnings": warnings,
    }
