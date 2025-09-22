from dataclasses import dataclass
from datetime import date
from src.domain.vo.location_code import LocationCode


@dataclass(frozen=True)
class FlightSearchParams:
    """Parameters for flight search"""
    origin: LocationCode
    destination: LocationCode
    departure_date: date
    adults: int = 1
    return_date: date | None = None
    children: int | None = None
    infants: int | None = None
    travel_class: str | None = None
    included_airline_codes: str | None = None
    excluded_airline_codes: str | None = None
    non_stop: bool | None = None
    currency_code: str | None = None
    max_price: int | None = None
    max_results: int | None = None
    
    def __post_init__(self):
        if self.adults < 1 or self.adults > 9:
            raise ValueError("Number of adults must be between 1 and 9")
        if self.children is not None and (self.children < 0 or self.children > 9):
            raise ValueError("Number of children must be between 0 and 9")
        if self.infants is not None and (self.infants < 0 or self.infants > 9):
            raise ValueError("Number of infants must be between 0 and 9")


@dataclass(frozen=True)
class CitySearchParams:
    """Parameters for city search"""
    keyword: str
    country_code: str | None = None
    max_results: int | None = None
    include: str | None = None
    
    def __post_init__(self):
        if len(self.keyword) < 2:
            raise ValueError("Keyword must have at least 2 characters")


