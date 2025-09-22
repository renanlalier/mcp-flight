from typing import List
from datetime import datetime
from src.domain.services.flight_search_service import FlightSearchService
from src.domain.vo.search_params import FlightSearchParams
from src.domain.vo.location_code import LocationCode
from src.application.dto.flight_dto import FlightSearchRequestDTO, FlightOfferDTO


class FlightApplicationService:
    """Application service for flights"""
    
    def __init__(self, flight_search_service: FlightSearchService):
        self._flight_search_service = flight_search_service
    
    async def search_flights(self, request: FlightSearchRequestDTO) -> List[FlightOfferDTO]:
        """Searches flights and returns DTOs"""
        # Converts DTO to Value Object
        params = FlightSearchParams(
            origin=LocationCode(request.origin_location_code),
            destination=LocationCode(request.destination_location_code),
            departure_date=datetime.fromisoformat(request.departure_date).date(),
            adults=request.adults,
            return_date=datetime.fromisoformat(request.return_date).date() if request.return_date else None,
            children=request.children,
            infants=request.infants,
            travel_class=request.travel_class,
            included_airline_codes=request.included_airline_codes,
            excluded_airline_codes=request.excluded_airline_codes,
            non_stop=request.non_stop,
            currency_code=request.currency_code,
            max_price=request.max_price,
            max_results=request.max_results
        )
        
        # Searches flights using domain service
        flights = await self._flight_search_service.search_best_flights(params)
        
        # Converts entities to DTOs
        return [self._map_flight_to_dto(flight) for flight in flights]
    
    def _map_flight_to_dto(self, flight) -> FlightOfferDTO:
        """Maps entity to DTO"""
        first_segment = flight.segments[0]
        last_segment = flight.segments[-1]
        
        return FlightOfferDTO(
            id=flight.id,
            origin=str(first_segment.departure),
            destination=str(last_segment.arrival),
            departure_time=first_segment.departure_time.isoformat(),
            arrival_time=last_segment.arrival_time.isoformat(),
            duration=flight.total_duration,
            price=flight.price,
            currency=flight.currency,
            airline=first_segment.carrier_code,
            flight_number=first_segment.flight_number,
            is_direct=flight.is_direct,
            seats_available=flight.seats_available,
            travel_class=flight.travel_class
        )
