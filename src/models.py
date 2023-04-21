"""Flight ticket related models."""

# Standard library
import typing
from datetime import date

# Third-party
import phonenumbers
import pydantic

# First-party
from src.enums import Cabin


class PhoneNumber(pydantic.BaseModel):
    """Model for a phone number."""

    country_code: str = "GB"
    value: str

    @pydantic.validator("value")
    @classmethod
    def validate_phone_number(
        cls, phone_number: str, values: dict[str, object]
    ) -> str:
        """Validate phone number.

        Raises:
            ValueError: Invalid phone number.
        """
        try:
            parsed_phone_number = phonenumbers.parse(
                phone_number, str(values.get("country_code"))
            )
        except phonenumbers.NumberParseException:
            raise ValueError(f"Invalid phone number")
        if phonenumbers.is_valid_number(parsed_phone_number):
            return phonenumbers.format_number(
                parsed_phone_number, phonenumbers.PhoneNumberFormat.E164
            )
        raise ValueError(f"Invalid phone number")


class FlightTicket(pydantic.BaseModel):
    """Model for a flight ticket."""

    first_name: str
    last_name: str
    pnr: str = pydantic.Field(regex="^[0-9a-zA-Z]{6}$")
    fare_class: str
    travel_date: date
    pax: int
    ticketing_date: date
    email: pydantic.EmailStr
    mobile_phone: PhoneNumber
    booked_cabin: Cabin

    class Config:
        """Flight ticket configuration."""

        fields = {
            "first_name": {"alias": "First_name"},
            "last_name": {"alias": "Last_name"},
            "pnr": {"alias": "PNR"},
            "fare_class": {"alias": "Fare_class"},
            "travel_date": {"alias": "Travel_date"},
            "pax": {"alias": "Pax"},
            "ticketing_date": {"alias": "Ticketing_date"},
            "email": {"alias": "Email"},
            "mobile_phone": {"alias": "Mobile_phone"},
            "booked_cabin": {"alias": "Booked_cabin"},
        }

        allow_population_by_field_name = True

    @pydantic.validator("ticketing_date")
    @classmethod
    def validate_ticketing_date(
        cls, ticketing_date: date, values: dict[str, object]
    ) -> date:
        """Validate ticketing date is before travel date.

        Raises:
            ValueError: Ticketing date is after travel date.
        """
        travel_date = typing.cast(date, values["travel_date"])
        if ticketing_date > travel_date:
            raise ValueError(f"Invalid ticketing date")
        return ticketing_date
