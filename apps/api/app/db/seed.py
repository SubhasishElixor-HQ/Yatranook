from sqlalchemy import null

from app.db.session import SessionLocal
from app.models.destination import Destination

SEED_DESTINATIONS = [
    {
      "district": "Gajapati",
      "state": "Odisha",
      "country": "India",
      "region": "Southern Odisha",
      "category": "Hill / trekking",
      "description": "Eastern Ghats hill landscape with heritage and trekking interest.",
      "coordinates": {
        "latitude": 18.99,
        "longitude": 84.38
      },
      "coordinate_status": "approximate_map_pin",
      "coordinate_reference_url": null,
      "coordinate_note": "Indicative map pin for discovery only; verify with a geocoder/local authority before route or distance calculations.",
      "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Mahendragiri%20Hills%2C%20Gajapati%2C%20Odisha%2C%20India",
      "openstreetmap_url": "https://www.openstreetmap.org/search?query=Mahendragiri%20Hills%2C%20Gajapati%2C%20Odisha%2C%20India",
      "opening_hours": null,
      "entry_fee_inr": null,
      "best_time_to_visit": null,
      "visitor_access_status": "check_before_visit",
      "data_completeness": "catalogue_name_and_category_curated; operational_details_unverified"
    },
    {
      "id": "OD-066",
      "name": "Talasari Beach",
      "district": "Balasore",
      "state": "Odisha",
      "country": "India",
      "region": "Coastal Odisha",
      "category": "Beach",
      "description": "Coastal beach near the Odisha–West Bengal border.",
      "coordinates": {
        "latitude": 21.5847,
        "longitude": 87.4489
      },
      "coordinate_status": "approximate_map_pin",
      "coordinate_reference_url": null,
      "coordinate_note": "Indicative map pin for discovery only; verify with a geocoder/local authority before route or distance calculations.",
      "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Talasari%20Beach%2C%20Balasore%2C%20Odisha%2C%20India",
      "openstreetmap_url": "https://www.openstreetmap.org/search?query=Talasari%20Beach%2C%20Balasore%2C%20Odisha%2C%20India",
      "opening_hours": null,
      "entry_fee_inr": null,
      "best_time_to_visit": null,
      "visitor_access_status": "check_before_visit",
      "data_completeness": "catalogue_name_and_category_curated; operational_details_unverified"
    },
    {
      "id": "OD-067",
      "name": "Tara Tarini Temple",
      "district": "Ganjam",
      "state": "Odisha",
      "country": "India",
      "region": "Coastal Odisha",
      "category": "Temple / pilgrimage",
      "description": "Hilltop Shakti shrine overlooking the Rushikulya river valley.",
      "coordinates": {
        "latitude": 19.4827,
        "longitude": 84.8864
      },
      "coordinate_status": "approximate_map_pin",
      "coordinate_reference_url": null,
      "coordinate_note": "Indicative map pin for discovery only; verify with a geocoder/local authority before route or distance calculations.",
      "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Tara%20Tarini%20Temple%2C%20Ganjam%2C%20Odisha%2C%20India",
      "openstreetmap_url": "https://www.openstreetmap.org/search?query=Tara%20Tarini%20Temple%2C%20Ganjam%2C%20Odisha%2C%20India",
      "opening_hours": null,
      "entry_fee_inr": null,
      "best_time_to_visit": null,
      "visitor_access_status": "check_before_visit",
      "data_completeness": "catalogue_name_and_category_curated; operational_details_unverified"
    },
    {
      "id": "OD-068",
      "name": "Tampara Lake",
      "district": "Ganjam",
      "state": "Odisha",
      "country": "India",
      "region": "Coastal Odisha",
      "category": "Lake / water recreation",
      "description": "Freshwater lake near Chatrapur with water-based recreation.",
      "coordinates": {
        "latitude": 19.515,
        "longitude": 84.875
      },
      "coordinate_status": "approximate_map_pin",
      "coordinate_reference_url": null,
      "coordinate_note": "Indicative map pin for discovery only; verify with a geocoder/local authority before route or distance calculations.",
      "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Tampara%20Lake%2C%20Ganjam%2C%20Odisha%2C%20India",
      "openstreetmap_url": "https://www.openstreetmap.org/search?query=Tampara%20Lake%2C%20Ganjam%2C%20Odisha%2C%20India",
      "opening_hours": null,
      "entry_fee_inr": null,
      "best_time_to_visit": null,
      "visitor_access_status": "check_before_visit",
      "data_completeness": "catalogue_name_and_category_curated; operational_details_unverified"
    },
    {
      "id": "OD-069",
      "name": "Udayagiri & Khandagiri Caves",
      "district": "Khordha",
      "state": "Odisha",
      "country": "India",
      "region": "Coastal Odisha",
      "category": "Cave / Jain heritage",
      "description": "Ancient rock-cut caves and inscriptions near Bhubaneswar.",
      "coordinates": {
        "latitude": 20.262831,
        "longitude": 85.78603
      },
      "coordinate_status": "reference_coordinate",
      "coordinate_reference_url": "https://newikis.com/en/List_of_Monuments_of_National_Importance_in_Odisha",
      "coordinate_note": "Reference point; verify exact entrance/visitor gate before navigation.",
      "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Udayagiri%20%26%20Khandagiri%20Caves%2C%20Khordha%2C%20Odisha%2C%20India",
      "openstreetmap_url": "https://www.openstreetmap.org/search?query=Udayagiri%20%26%20Khandagiri%20Caves%2C%20Khordha%2C%20Odisha%2C%20India",
      "opening_hours": null,
      "entry_fee_inr": null,
      "best_time_to_visit": null,
      "visitor_access_status": "check_before_visit",
      "data_completeness": "catalogue_name_and_category_curated; operational_details_unverified"
    },
    {
      "id": "OD-070",
      "name": "Midhubandha Waterfall",
      "district": "Kalahandi",
      "state": "Odisha",
      "country": "India",
      "region": "Western Odisha",
      "category": "Waterfall",
      "description": "Waterfall attraction in the Kalahandi region; coordinate is indicative.",
      "coordinates": {
        "latitude": 19.8,
        "longitude": 83.2
      },
      "coordinate_status": "approximate_map_pin",
      "coordinate_reference_url": null,
      "coordinate_note": "Indicative map pin for discovery only; verify with a geocoder/local authority before route or distance calculations.",
      "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Midhubandha%20Waterfall%2C%20Kalahandi%2C%20Odisha%2C%20India",
      "openstreetmap_url": "https://www.openstreetmap.org/search?query=Midhubandha%20Waterfall%2C%20Kalahandi%2C%20Odisha%2C%20India",
      "opening_hours": null,
      "entry_fee_inr": null,
      "best_time_to_visit": null,
      "visitor_access_status": "check_before_visit",
      "data_completeness": "catalogue_name_and_category_curated; operational_details_unverified"
    },
    {
      "id": "OD-071",
      "name": "Minajhola",
      "district": "Rayagada",
      "state": "Odisha",
      "country": "India",
      "region": "Southern Odisha",
      "category": "Scenic / river confluence",
      "description": "Scenic river confluence and pilgrimage area.",
      "coordinates": {
        "latitude": 19.2,
        "longitude": 83.68
      },
      "coordinate_status": "approximate_map_pin",
      "coordinate_reference_url": null,
      "coordinate_note": "Indicative map pin for discovery only; verify with a geocoder/local authority before route or distance calculations.",
      "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Minajhola%2C%20Rayagada%2C%20Odisha%2C%20India",
      "openstreetmap_url": "https://www.openstreetmap.org/search?query=Minajhola%2C%20Rayagada%2C%20Odisha%2C%20India",
      "opening_hours": null,
      "entry_fee_inr": null,
      "best_time_to_visit": null,
      "visitor_access_status": "check_before_visit",
      "data_completeness": "catalogue_name_and_category_curated; operational_details_unverified"
    },
    {
      "id": "OD-072",
      "name": "Mukteswara Temple",
      "district": "Khordha",
      "state": "Odisha",
      "country": "India",
      "region": "Coastal Odisha",
      "category": "Temple / heritage",
      "description": "Ornate 10th-century temple in Bhubaneswar.",
      "coordinates": {
        "latitude": 20.2383,
        "longitude": 85.837
      },
      "coordinate_status": "approximate_map_pin",
      "coordinate_reference_url": null,
      "coordinate_note": "Indicative map pin for discovery only; verify with a geocoder/local authority before route or distance calculations.",
      "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Mukteswara%20Temple%2C%20Khordha%2C%20Odisha%2C%20India",
      "openstreetmap_url": "https://www.openstreetmap.org/search?query=Mukteswara%20Temple%2C%20Khordha%2C%20Odisha%2C%20India",
      "opening_hours": null,
      "entry_fee_inr": null,
      "best_time_to_visit": null,
      "visitor_access_status": "check_before_visit",
      "data_completeness": "catalogue_name_and_category_curated; operational_details_unverified"
    },
    {
      "id": "OD-073",
      "name": "Museum Of Justice",
      "district": "Bhubaneswar",
      "state": "Odisha",
      "country": "India",
      "region": "Coastal Odisha",
      "category": "Museum / cultural",
      "description": "Museum dedicated to the history and evolution of the justice system in India.",
      "coordinates": {
        "latitude": 20.265,
        "longitude": 85.817
      },
      "coordinate_status": "approximate_map_pin",
      "coordinate_reference_url": null,
      "coordinate_note": "Indicative map pin for discovery only; verify with a geocoder/local authority before route or distance calculations.",
      "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Museum%20Of%20Justice%2C%20Bhubaneswar%2C%20Odisha%2C%20India",
      "openstreetmap_url": "https://www.openstreetmap.org/search?query=Museum%20Of%20Justice%2C%20Bhubaneswar%2C%20Odisha%2C%20India",
      "opening_hours": null,
      "entry_fee_inr": null,
      "best_time_to_visit": null,
      "visitor_access_status": "check_before_visit",
      "data_completeness": "catalogue_name_and_category_curated; operational_details_unverified"
    }
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
