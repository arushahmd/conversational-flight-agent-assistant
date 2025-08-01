"""
    Contains the agents and tools to interact with aviation stack free API
"""

import os
import requests
from dotenv import load_dotenv
from datetime import date
from typing import Optional, Dict, Any

class AviationStackAPI:
    def __init__(self, params: Optional[Dict[str, Any]] = None) -> None:
        load_dotenv()
        self.api_key = os.getenv("AVIATION_API_KEY")
        self.flight_url = "https://api.aviationstack.com/v1/flights"
        self.airline_url = "https://api.aviationstack.com/v1/airlines"

        self.params = params.copy() if params else {}
        default_date = date.today().isoformat()
        default_limit = 2
        # self.params.setdefault("flight_date", default_date)
        self.params.setdefault("limit", default_limit)
        self.params["access_key"] = self.api_key

    def get_flights(self) -> Dict:
        """Get flight listings based on current parameters."""
        response = requests.get(self.flight_url, params=self.params)
        response.raise_for_status()
        return response.json()

    def get_flight_detail(self) -> Dict:
        """Alias for fetching a detailed flight (maybe a specific one)."""
        return self.get_flights()

    def get_airlines(self) -> Dict:
        """Fetch airline information."""
        response = requests.get(self.airline_url, params=self.params)
        response.raise_for_status()
        return response.json()

