import logging
from mcp.server.fastmcp import FastMCP

from src.application.dto.flight_dto import FlightSearchRequestDTO
from src.domain.vo.search_params import CitySearchParams
from src.domain.exceptions.flight_exceptions import (
    InvalidSearchParametersException,
    FlightServiceUnavailableException,
    FlightApiException
)
from src.infrastructure.container import container

logger = logging.getLogger(__name__)


def register_tools(mcp: FastMCP):
    """Registers MCP tools"""
    
    @mcp.tool()
    async def search_flights(
        origin_location_code: str,
        destination_location_code: str,
        departure_date: str,
        adults: int = 1,
        return_date: str | None = None,
        children: int = 0,
        infants: int = 0,
        travel_class: str | None = None,
        included_airline_codes: str | None = None,
        excluded_airline_codes: str | None = None,
        non_stop: bool = False,
        currency_code: str | None = None,
        max_price: int | None = None,
        max_results: int = 20
    ) -> dict:
        """Searches flight offers using Amadeus API."""
        try:
            request = FlightSearchRequestDTO(
                origin_location_code=origin_location_code,
                destination_location_code=destination_location_code,
                departure_date=departure_date,
                adults=adults,
                return_date=return_date,
                children=children,
                infants=infants,
                travel_class=travel_class,
                included_airline_codes=included_airline_codes,
                excluded_airline_codes=excluded_airline_codes,
                non_stop=non_stop,
                currency_code=currency_code,
                max_price=max_price,
                max_results=max_results
            )
            
            flights = await container.flight_app_service.search_flights(request)
            return {"flights": [flight.__dict__ for flight in flights]}
            
        except InvalidSearchParametersException as e:
            logger.warning("Invalid parameters for flight search: %s", str(e))
            return {"error": str(e)}
        except FlightServiceUnavailableException as e:
            logger.error("Flight service unavailable: %s", str(e))
            return {"error": str(e)}
        except FlightApiException as e:
            logger.error("Flight API error: %s", str(e))
            return {"error": str(e)}
    
    @mcp.tool()
    async def search_cities(
        keyword: str,
        country_code: str | None = None,
        max_results: int = 10,
        include: str = "AIRPORTS"
    ) -> dict:
        """
        Searches city and airport data using Amadeus API.
        """
        params = CitySearchParams(
            keyword=keyword,
            country_code=country_code,
            max_results=max_results,
            include=include
        )

        try:
            result = await container.city_gateway.search_cities(params)
            return result
        except InvalidSearchParametersException as e:
            logger.warning("Invalid parameters for city search: %s", str(e))
            return {"error": str(e)}
        except FlightServiceUnavailableException as e:
            logger.error("City service unavailable: %s", str(e))
            return {"error": str(e)}
        except FlightApiException as e:
            logger.error("City API error: %s", str(e))
            return {"error": str(e)}
