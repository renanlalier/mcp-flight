from typing import List
from src.domain.entities.flight import FlightOffer
from src.domain.gateways.flight_gateway import FlightGateway
from src.domain.vo.search_params import FlightSearchParams


class FlightSearchService:
    """Domain service for flight search"""
    
    def __init__(self, flight_gateway: FlightGateway):
        self._flight_gateway = flight_gateway
    
    async def search_best_flights(self, params: FlightSearchParams) -> List[FlightOffer]:
        """Searches the best flights based on parameters"""
        flights = await self._flight_gateway.search_flights(params)
        
        # Apply business rules to sort/filter
        return self._sort_flights_by_best_value(flights)
    
    def _sort_flights_by_best_value(self, flights: List[FlightOffer]) -> List[FlightOffer]:
        """Sorts flights by best value"""
        # Prioritizes direct flights and lower price
        return sorted(flights, key=lambda f: (not f.is_direct, f.price))
