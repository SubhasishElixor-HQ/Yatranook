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
