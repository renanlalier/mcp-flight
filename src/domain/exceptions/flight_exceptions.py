"""Flight domain exceptions"""


class FlightDomainException(Exception):
    """Base exception for flight domain"""
    pass


class InvalidSearchParametersException(FlightDomainException):
    """Exception for invalid search parameters"""
    pass


class FlightServiceUnavailableException(FlightDomainException):
    """Exception for when flight service is unavailable"""
    pass


class FlightApiException(FlightDomainException):
    """Exception for external flight API errors"""
    
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code
