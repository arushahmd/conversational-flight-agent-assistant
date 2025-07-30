import json
from heapq import nlargest
from typing import List, Dict, Any

def load_flights(filepath="data/flights.json"):
    """
        Load json flights data file
    """
    with open(filepath, "r") as f:
        return json.load(f)


def get_available_routes() -> List[str]:
    """
        get list of all available routes
    """
    flights = load_flights()
    seen = set()
    routes = []
    for flight in flights:
        origin = flight["from"].strip()
        destination = flight["to"].strip()
        route = (origin, destination)
        if route not in seen:
            seen.add(route)
            routes.append(f"{origin} → {destination}")
    return routes


def score_flight(flight: Dict[str, Any]) -> float:
    """
    Define your custom scoring logic here.
    For example: lower price and shorter duration = better score.
    You can adapt this as needed.
    """
    price_score = 1 / (flight.get("price", 1000) + 1)
    duration_score = 1 / (flight.get("duration", 999) + 1)
    rating_score = flight.get("airline_rating", 0) / 5  # Optional

    return 0.5 * price_score + 0.3 * duration_score + 0.2 * rating_score


def match_flights(queries: List[Dict[str, Any]], flights: List[Dict[str, Any]], top_k: int = 2) -> List[Dict[str, Any]]:
    """
    Takes a list of flight search queries and returns top matching flights for each valid query.
    Filters flights that match 'from' and 'to' fields exactly before scoring.

    Returns a flat list of top-k results for each query.
    """
    matched_results = []

    for query in queries:
        origin = query.get("origin", "").strip().lower()
        destination = query.get("destination", "").strip().lower()

        if not origin or not destination:
            continue  # skip invalid query

        filtered = [
            flight for flight in flights
            if flight.get("from", "").strip().lower() == origin and
               flight.get("to", "").strip().lower() == destination
        ]

        if not filtered:
            continue  # skip if no matching routes

        scored = sorted(filtered, key=score_flight, reverse=True)
        matched_results.extend(scored[:top_k])

    return matched_results


