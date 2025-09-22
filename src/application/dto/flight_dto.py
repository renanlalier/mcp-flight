from dataclasses import dataclass
from datetime import date


@dataclass
class FlightSearchRequestDTO:
    """DTO for flight search request"""
    origin_location_code: str
    destination_location_code: str
    departure_date: str
    adults: int = 1
    return_date: str | None = None
    children: int | None = None
    infants: int | None = None
    travel_class: str | None = None
    included_airline_codes: str | None = None
    excluded_airline_codes: str | None = None
    non_stop: bool | None = None
    currency_code: str | None = None
    max_price: int | None = None
    max_results: int | None = None


@dataclass
class FlightOfferDTO:
    """DTO for flight offer"""
    id: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    duration: str
    price: float
    currency: str
    airline: str
    flight_number: str
    is_direct: bool
    seats_available: int
    travel_class: str
