from dataclasses import dataclass
from datetime import datetime
from src.domain.vo.location_code import LocationCode


@dataclass
class FlightSegment:
    """Flight segment"""
    departure: LocationCode
    arrival: LocationCode
    departure_time: datetime
    arrival_time: datetime
    carrier_code: str
    flight_number: str
    aircraft: str | None = None
    duration: str | None = None


@dataclass
class FlightOffer:
    """Flight offer"""
    id: str
    segments: list[FlightSegment]
    price: float
    currency: str
    seats_available: int
    travel_class: str
    validating_airline_codes: list[str]
    instant_ticketing_required: bool = False
    non_homogeneous: bool = False
    one_way: bool = False
    last_ticketing_date: str | None = None
    
    @property
    def total_duration(self) -> str:
        """Total flight duration"""
        if not self.segments:
            return "0H00M"
        
        first_departure = self.segments[0].departure_time
        last_arrival = self.segments[-1].arrival_time
        duration = last_arrival - first_departure
        
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        return f"{hours}H{minutes:02d}M"
    
    @property
    def is_direct(self) -> bool:
        """Checks if it's a direct flight"""
        return len(self.segments) == 1
