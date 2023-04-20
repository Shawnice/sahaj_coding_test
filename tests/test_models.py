"""Test suite for `src.models`."""

# Third-party
import pytest

# First-party
from src.models import FlightTicket, PhoneNumber


class TestPhoneNumber:
    """Tests for `src.models.PhoneNumber`."""

    @pytest.mark.parametrize(
        "uk_phone_number, expected",
        [
            ("7448212116", "+447448212116"),
            ("07448212116", "+447448212116"),
            ("+447448212116", "+447448212116"),
        ],
    )
    def test_validate_phone_number(
        self, uk_phone_number: str, expected: str
    ) -> None:
        """Assert method validates a phone number correctly."""
        parsed_number = PhoneNumber(value=uk_phone_number)
        assert parsed_number.value == expected

    def test_validate_invalid_phone_number(self) -> None:
        """Assert method raises an error on invalid phone number."""
        with pytest.raises(ValueError):
            PhoneNumber(value="9876543210")


class TestFlightTicket:
    """Tests for `src.models.FlightTicket`."""

    def test_valid_ticket_flight(
        self, sample_flight_ticket_data: dict[str, object]
    ) -> None:
        """Assert instantiate `FlightTicket` object successfully."""
        flight_ticket = FlightTicket(**sample_flight_ticket_data)
        assert (
            flight_ticket.first_name == sample_flight_ticket_data["First_name"]
        )
        assert (
            flight_ticket.fare_class == sample_flight_ticket_data["Fare_class"]
        )
        assert flight_ticket.email == sample_flight_ticket_data["Email"]

    @pytest.mark.parametrize(
        "pnr",
        [
            "ZZZ",
            "12*AB&"
            "111Y2Z4D",
        ],
    )
    def test_invalid_pnr(
        self, pnr: str, sample_flight_ticket_data: dict[str, object]
    ) -> None:
        """Assert model raises an error on invalid PNR."""
        sample_flight_ticket_data["PNR"] = pnr
        with pytest.raises(ValueError):
            FlightTicket(**sample_flight_ticket_data)

    @pytest.mark.parametrize(
        "email",
        ["hello@email", "hello@baddash.-.com", "hello@.leadingdot.com"],
    )
    def test_invalid_email(
        self, email: str, sample_flight_ticket_data: dict[str, object]
    ) -> None:
        """Assert model raises an error on invalid email."""
        sample_flight_ticket_data["Email"] = email
        with pytest.raises(ValueError):
            FlightTicket(**sample_flight_ticket_data)

    @pytest.mark.parametrize(
        "cabin",
        [
            "Unknown Cabin",
            "business",
        ],
    )
    def test_invalid_booked_cabin(
        self, cabin: str, sample_flight_ticket_data: dict[str, object]
    ) -> None:
        """Assert model raises an error on invalid booked cabin."""
        sample_flight_ticket_data["Booked_cabin"] = cabin
        with pytest.raises(ValueError):
            FlightTicket(**sample_flight_ticket_data)

    def test_invalid_flight_ticket_data(
        self, sample_flight_ticket_data: dict[str, object]
    ) -> None:
        """Assert model raises an error on invalid flight ticket data."""
        sample_flight_ticket_data["Ticketing_date"] = "2019-08-01"
        with pytest.raises(ValueError):
            FlightTicket(**sample_flight_ticket_data)
