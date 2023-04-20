"""Enumeration for a flight ticket."""

# Standard library
from enum import StrEnum


class Cabin(StrEnum):
    """Possible cabin types of a flight."""

    ECONOMY: str = "Economy"
    PREMIUM_ECONOMY: str = "Premium Economy"
    BUSINESS: str = "Business"
    FIRST: str = "First"


class DiscountCode(StrEnum):
    """Possible discount codes for a flight."""

    OFFER_20: str = "OFFER_20"
    OFFER_30: str = "OFFER_30"
    OFFER_25: str = "OFFER_25"
