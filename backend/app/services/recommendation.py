from collections.abc import Iterable

from app.models.brand import Brand
from app.models.collection_item import CollectionItem
from app.models.fragrance import Fragrance
from app.schemas.recommendation import RecommendationRequest


def build_recommendations(rows: Iterable, payload: RecommendationRequest) -> list[dict]:
    grouped = {}

    for item, fragrance, brand, tag in rows:
        key = item.id

        if key not in grouped:
            grouped[key] = {
                "item": item,
                "fragrance": fragrance,
                "brand": brand,
                "tags": set(),
            }

        grouped[key]["tags"].add((tag.type, tag.name))

    scored = []

    for data in grouped.values():
        item: CollectionItem = data["item"]
        fragrance: Fragrance = data["fragrance"]
        brand: Brand = data["brand"]
        tags = data["tags"]

        score = 0
        penalty = min(item.times_worn, 5)
        matched_context = []

        if ("occasion", payload.occasion) in tags:
            score += 5
            matched_context.append(f"{payload.occasion} occasion")
        if ("weather", payload.weather) in tags:
            score += 5
            matched_context.append(f"{payload.weather} weather")
        if ("season", payload.season) in tags:
            score += 3
            matched_context.append(f"{payload.season} season")
        if ("time_of_day", payload.time_of_day) in tags:
            score += 3
            matched_context.append(f"{payload.time_of_day} time")
        if ("location_type", payload.location_type) in tags:
            score += 3
            matched_context.append(f"{payload.location_type} setting")

        rating_bonus = min(item.personal_rating or 0, 3)
        score += rating_bonus
        score -= penalty

        reason_parts = []
        if matched_context:
            reason_parts.append("Matches " + ", ".join(matched_context[:3]))
        if item.personal_rating and item.personal_rating >= 8:
            reason_parts.append("highly rated by you")
        if item.times_worn <= 1:
            reason_parts.append("not overused recently")

        reason = (
            ". ".join(reason_parts)
            if reason_parts
            else "Best available match from your collection"
        )

        scored.append(
            {
                "item": item,
                "fragrance": fragrance,
                "brand": brand,
                "score": score,
                "reason": reason,
            }
        )

    scored.sort(
        key=lambda entry: (
            entry["score"],
            -entry["item"].times_worn,
        ),
        reverse=True,
    )

    return scored[:3]
