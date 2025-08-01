from langchain.tools import Tool
from aviationstack import AviationStackAPI

aviation_flight_tool = Tool(
    name="aviation-api-tool",
    func=lambda params: AviationStackAPI(params).get_flights(),
    description="Use this tool to get live flight details from AviationStack API given origin, destination, date, etc."
)


if __name__  == "__main__":
    params = {
        # "flight_date": "2025-08-01",
        # "limit":1,
        # "airline_name": "American Airlines"
    }
    params = None

    result = aviation_flight_tool.func(params) # type: ignore
    print(result)
