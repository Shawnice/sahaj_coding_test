"""Fixtures for flight ticket application."""

# Standard library
import pathlib

# Third-party
import pytest

# First-party
from src.flights import get_flight_ticket_data


@pytest.fixture()
def sample_flight_ticket_data_path() -> pathlib.Path:
    """Return a path to the flight ticket data file."""
    return pathlib.Path(__file__).parent / "flight-ticket-data.csv"


@pytest.fixture()
def sample_flight_ticket_data() -> dict[str, object]:
    """Return sample flight ticket data."""
    return {
        "First_name": "Abhishek",
        "Last_name": "Kumar",
        "PNR": "ABC123",
        "Fare_class": "F",
        "Travel_date": "2019-07-31",
        "Pax": "2",
        "Ticketing_date": "2019-05-21",
        "Email": "abhishek@zzz.com",
        "Mobile_phone": {"value": "7448212116"},
        "Booked_cabin": "Economy",
    }


@pytest.fixture()
def invalid_flight_ticket_data() -> dict[str, object]:
    """Return invalid flight ticket data."""
    return {
        "First_name": "Monin",
        "Last_name": "Sankar",
        "PNR": "PQ234",
        "Fare_class": "F",
        "Travel_date": "2019-07-31",
        "Pax": "2",
        "Ticketing_date": "2019-08-01",
        "Email": "abhishek@zzz",
        "Mobile_phone": {"value": "0000000000"},
        "Booked_cabin": "Second",
    }
