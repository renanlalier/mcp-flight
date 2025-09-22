"""Dependency container for dependency injection"""

from src.application.services.flight_application_service import FlightApplicationService
from src.infrastructure.gateways.amadeus_flight_gateway import AmadeusFlightGateway
from src.infrastructure.gateways.amadeus_city_gateway import AmadeusCityGateway
from src.domain.services.flight_search_service import FlightSearchService


class Container:
    """Dependency container using lazy initialization"""
    
    def __init__(self):
        self._flight_gateway: AmadeusFlightGateway | None = None
        self._city_gateway: AmadeusCityGateway | None = None
        self._flight_search_service: FlightSearchService | None = None
        self._flight_app_service: FlightApplicationService | None = None
    
    @property
    def flight_gateway(self) -> AmadeusFlightGateway:
        if self._flight_gateway is None:
            self._flight_gateway = AmadeusFlightGateway()
        return self._flight_gateway
    
    @property
    def city_gateway(self) -> AmadeusCityGateway:
        if self._city_gateway is None:
            self._city_gateway = AmadeusCityGateway()
        return self._city_gateway
    
    @property
    def flight_search_service(self) -> FlightSearchService:
        if self._flight_search_service is None:
            self._flight_search_service = FlightSearchService(self.flight_gateway)
        return self._flight_search_service
    
    @property
    def flight_app_service(self) -> FlightApplicationService:
        if self._flight_app_service is None:
            self._flight_app_service = FlightApplicationService(self.flight_search_service)
        return self._flight_app_service
    


# Global container instance
container = Container()
