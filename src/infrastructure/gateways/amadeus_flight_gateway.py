from typing import List
from datetime import datetime
from src.domain.entities.flight import FlightOffer, FlightSegment
from src.domain.gateways.flight_gateway import FlightGateway
from src.domain.vo.search_params import FlightSearchParams
from src.domain.vo.location_code import LocationCode
from src.infrastructure.external.amadeus_client import AmadeusClient


class AmadeusFlightGateway(FlightGateway):
    """Flight gateway implementation using Amadeus API"""
    
    def __init__(self):
        self._client = AmadeusClient()
    
    async def search_flights(self, params: FlightSearchParams) -> List[FlightOffer]:
        """Searches flight offers in Amadeus API"""
        api_params = self._build_api_params(params)
        response = await self._client.get("/v2/shopping/flight-offers", api_params)
        
        return self._map_response_to_entities(response)
    
    def _build_api_params(self, params: FlightSearchParams) -> dict:
        """Builds parameters for API"""
        api_params = {
            "originLocationCode": str(params.origin),
            "destinationLocationCode": str(params.destination),
            "departureDate": params.departure_date.isoformat(),
            "adults": params.adults
        }
        
        # Optional parameters
        if params.return_date:
            api_params["returnDate"] = params.return_date.isoformat()
        if params.children is not None:
            api_params["children"] = params.children
        if params.infants is not None:
            api_params["infants"] = params.infants
        if params.travel_class:
            api_params["travelClass"] = params.travel_class
        if params.included_airline_codes:
            api_params["includedAirlineCodes"] = params.included_airline_codes
        if params.excluded_airline_codes:
            api_params["excludedAirlineCodes"] = params.excluded_airline_codes
        if params.non_stop is not None:
            api_params["nonStop"] = params.non_stop
        if params.currency_code:
            api_params["currencyCode"] = params.currency_code
        if params.max_price is not None:
            api_params["maxPrice"] = params.max_price
        if params.max_results is not None:
            api_params["max"] = params.max_results
        
        return api_params
    
    def _map_response_to_entities(self, response: dict) -> List[FlightOffer]:
        """Maps API response to entities"""
        offers = []
        
        for offer_data in response.get("data", []):
            segments = []
            
            for itinerary in offer_data.get("itineraries", []):
                for segment_data in itinerary.get("segments", []):
                    segment = FlightSegment(
                        departure=LocationCode(segment_data["departure"]["iataCode"]),
                        arrival=LocationCode(segment_data["arrival"]["iataCode"]),
                        departure_time=datetime.fromisoformat(
                            segment_data["departure"]["at"].replace("Z", "+00:00")
                        ),
                        arrival_time=datetime.fromisoformat(
                            segment_data["arrival"]["at"].replace("Z", "+00:00")
                        ),
                        carrier_code=segment_data["carrierCode"],
                        flight_number=segment_data["number"],
                        aircraft=segment_data.get("aircraft", {}).get("code"),
                        duration=segment_data.get("duration")
                    )
                    segments.append(segment)
            
            price_data = offer_data["price"]
            offer = FlightOffer(
                id=offer_data["id"],
                segments=segments,
                price=float(price_data["total"]),
                currency=price_data["currency"],
                seats_available=offer_data.get("numberOfBookableSeats", 0),
                travel_class=offer_data.get("travelerPricings", [{}])[0].get("fareDetailsBySegment", [{}])[0].get("class", ""),
                validating_airline_codes=offer_data.get("validatingAirlineCodes", []),
                instant_ticketing_required=offer_data.get("instantTicketingRequired", False),
                non_homogeneous=offer_data.get("nonHomogeneous", False),
                one_way=offer_data.get("oneWay", False),
                last_ticketing_date=offer_data.get("lastTicketingDate")
            )
            offers.append(offer)
        
        return offers
