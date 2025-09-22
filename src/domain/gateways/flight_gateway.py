from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.flight import FlightOffer
from src.domain.vo.search_params import FlightSearchParams


class FlightGateway(ABC):
    """Interface do gateway de voos para API externa"""
    
    @abstractmethod
    async def search_flights(self, params: FlightSearchParams) -> List[FlightOffer]:
        """Busca ofertas de voos via API externa"""
        pass
