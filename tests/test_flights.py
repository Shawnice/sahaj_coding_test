"""Test suite for `src.flights`."""

# Standard library
import pathlib
import unittest.mock

# Third-party
import pydantic
import pytest

# First-party
import src.typings
from src.flights import (
    gen_discount_code,
    get_flight_ticket_data,
    handle_errors,
    validate_flight_ticket_data,
)
from src.models import FlightTicket


def test_get_flight_ticket_data(
    sample_flight_ticket_data_path: pathlib.Path,
) -> None:
    """Assert method processes input csv file correctly."""
    ticket_data = get_flight_ticket_data(sample_flight_ticket_data_path)
    assert len(ticket_data) == 5
    assert ticket_data[0]["Email"] == "abhishek@zzz.com"
    assert ticket_data[0]["First_name"] == "Abhishek"


def test_get_flight_ticket_data__error() -> None:
    """Assert method raises error if file is not found."""
    with pytest.raises(FileNotFoundError):
        get_flight_ticket_data(pathlib.Path("non_existent_file.csv"))


def test_handle_error(
    sample_flight_ticket_data: dict[str, object],
    invalid_flight_ticket_data: dict[str, object],
) -> None:
    """Assert method returns expected error codes."""
    try:
        FlightTicket(**invalid_flight_ticket_data)
    except pydantic.ValidationError as exc:
        error_codes = handle_errors(exc)
        assert error_codes == (
            "Invalid PNR,Invalid ticketing date,"
            + "Invalid email,Invalid phone number,Invalid Booked_cabin"
        )


@pytest.mark.parametrize(
    "fare_class, expected_discount_code",
    [
        ("A", "OFFER_20"),
        ("E", "OFFER_20"),
        ("F", "OFFER_30"),
        ("K", "OFFER_30"),
        ("L", "OFFER_25"),
        ("R", "OFFER_25"),
        ("Z", ""),
    ],
)
def test_gen_discount_code(
    fare_class: str, expected_discount_code: str
) -> None:
    """Assert method returns correct discount code."""
    assert gen_discount_code(fare_class) == expected_discount_code


def test_validate_flight_ticket_data() -> None:
    """Assert method validates flight ticket data correctly."""
    pass