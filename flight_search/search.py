import json
from heapq import nlargest
from typing import List, Dict, Any

def load_flights(filepath="data/flights.json"):
    """
        Load json flights data file
    """
    with open(filepath, "r") as f:
        return json.load(f)

def match_flights(query: Dict[str, Any], flights: List[Dict[str, Any]], top_k: int = 2) -> List[Dict[str, Any]]:
    """
        Return top k, 2 for now matching flights from the stored json data.
    """
    def calculate_score(query: Dict[str, Any], flight: Dict[str, Any]) -> int:
        score = 0

        if query.get("origin") and query["origin"].lower() in flight.get("from", "").lower():
            score += 1

        if query.get("destination") and query["destination"].lower() in flight.get("to", "").lower():
            score += 1

        if query.get("departure_date") == flight.get("departure_date"):
            score += 1

        if query.get("return_date") == flight.get("return_date"):
            score += 1

        if query.get("refundable") and flight.get("refundable"):
            score += 1

        if query.get("alliance") and query["alliance"].lower() in flight.get("alliance", "").lower():
            score += 1

        if query.get("layovers"):
            flight_layovers = [l.lower() for l in flight.get("layovers", [])]
            if any(lay.lower() in flight_layovers for lay in query["layovers"]):
                score += 1

        return score

    # Score all flights
    scored = [(calculate_score(query, flight), flight) for flight in flights]

    # Filter out flights with zero score
    scored = [item for item in scored if item[0] > 0]

    # Get top-k by score
    top_matches = nlargest(top_k, scored, key=lambda x: x[0])

    # Return only the flight dictionaries
    return [flight for _, flight in top_matches]

