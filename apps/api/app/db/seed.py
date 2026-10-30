from app.db.session import SessionLocal
from app.models.destination import Destination

SEED_DESTINATIONS = [
    {
        "id": "konark", "name": "Konark Sun Temple", "location": "Konark, Odisha", "region": "Odisha", "category": "Heritage",
        "description": "A celebrated 13th-century temple complex known for its monumental stone architecture and chariot-inspired design.",
        "image": "https://images.unsplash.com/photo-1606293926075-69a00dbfde81?auto=format&fit=crop&w=1000&q=85",
        "latitude": 19.8876, "longitude": 86.0945, "duration": "1.5–2 hours", "price_label": "Verify current visitor fees and access rules",
        "tags": ["Architecture", "History", "UNESCO", "Temple"], "source_name": "Seed catalogue; verify with official tourism sources",
    },
    {
        "id": "puri-beach", "name": "Puri Beach", "location": "Puri, Odisha", "region": "Odisha", "category": "Beach",
        "description": "A popular coastline for sea views, beach walks, and nearby local food experiences.",
        "image": "https://images.unsplash.com/photo-1519046904884-53103b34b206?auto=format&fit=crop&w=1000&q=85",
        "latitude": 19.7983, "longitude": 85.8249, "duration": "1–2 hours", "price_label": "Public beach access; verify activity costs",
        "tags": ["Coastline", "Beach", "Sunrise", "Food"], "source_name": "Seed catalogue; verify with official tourism sources",
    },
    {
        "id": "chilika-satapada", "name": "Chilika Lake — Satapada", "location": "Satapada, Odisha", "region": "Odisha", "category": "Nature",
        "description": "A coastal lagoon landscape known for boating experiences and seasonal birdlife; service details require current verification.",
        "image": "https://images.unsplash.com/photo-1501785888041-af3ef285f470?auto=format&fit=crop&w=1000&q=85",
        "latitude": 19.6725, "longitude": 85.3205, "duration": "Half day", "price_label": "Boat and activity costs vary; verify with operator",
        "tags": ["Lake", "Birdlife", "Nature", "Boat"], "source_name": "Seed catalogue; verify with official tourism sources",
    },
    {
        "id": "lingaraj", "name": "Lingaraj Temple", "location": "Old Town, Bhubaneswar, Odisha", "region": "Odisha", "category": "Temple",
        "description": "A major temple complex associated with Kalinga architecture. Visitor access rules should be checked before travel.",
        "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=1000&q=85",
        "latitude": 20.2376, "longitude": 85.8348, "duration": "45–90 minutes", "price_label": "Verify visitor access rules",
        "tags": ["Temple", "Architecture", "Culture", "Heritage"], "source_name": "Seed catalogue; verify with official tourism sources",
    },
    {
        "id": "dhauli", "name": "Dhauli Shanti Stupa", "location": "Dhauli, Bhubaneswar, Odisha", "region": "Odisha", "category": "Heritage",
        "description": "A hilltop peace pagoda associated with the Kalinga War and the history of Emperor Ashoka.",
        "image": "https://images.unsplash.com/photo-1590050752117-23a9d709bb31?auto=format&fit=crop&w=1000&q=85",
        "latitude": 20.1920, "longitude": 85.8390, "duration": "45–60 minutes", "price_label": "Verify current access and transport details",
        "tags": ["History", "Peace", "Viewpoint", "Heritage"], "source_name": "Seed catalogue; verify with official tourism sources",
    },
    {
        "id": "nandankanan", "name": "Nandankanan", "location": "Bhubaneswar, Odisha", "region": "Odisha", "category": "Wildlife",
        "description": "A zoological and botanical destination offering wildlife and nature experiences; current ticket and safari details should be checked.",
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1000&q=85",
        "latitude": 20.3974, "longitude": 85.8180, "duration": "3–4 hours", "price_label": "Entry and activity fees vary; verify before visiting",
        "tags": ["Wildlife", "Family", "Nature"], "source_name": "Seed catalogue; verify with official tourism sources",
    },
]


def seed_destinations() -> None:
    with SessionLocal() as db:
        for record in SEED_DESTINATIONS:
            existing = db.get(Destination, record["id"])
            if existing is None:
                db.add(Destination(**record))
        db.commit()


if __name__ == "__main__":
    seed_destinations()
    print("Destination seed complete.")
