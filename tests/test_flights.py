"""Test suite for `src.flights`."""

# Standard library
import os
import pathlib
import typing

# Third-party
import pydantic
import pytest

# First-party
import src.typings
from src.flights import (gen_discount_code, get_flight_ticket_data,
                         handle_errors, output_invalid_flight_ticket_data,
                         output_valid_flight_ticket_data,
                         validate_flight_ticket_data)
from src.models import FlightTicket

BASE_OUTPUT_HEADERS = (
    "First_name,Last_name,PNR,Fare_class,Travel_date,Pax,"
    + "Ticketing_date,Email,Mobile_phone,Booked_cabin"
)


def test_get_flight_ticket_data(
    sample_flight_ticket_data_path: pathlib.Path,
) -> None:
    """Assert method processes input csv file correctly."""
    ticket_data = get_flight_ticket_data(sample_flight_ticket_data_path)
    assert len(ticket_data) == 9
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


@pytest.mark.parametrize(
    "method, flight_ticket_data, file_name, new_header, new_column_value",
    [
        (
            output_valid_flight_ticket_data,
            pytest.lazy_fixture("sample_flight_ticket_data"),
            "valid-flight-tickets",
            "Discount_code",
            "OFFER_20",
        ),
        (
            output_invalid_flight_ticket_data,
            pytest.lazy_fixture("invalid_flight_ticket_data"),
            "invalid-flight-tickets",
            "Error",
            "Invalid email",
        ),
    ],
)
def test_output_valid_and_invalid_flight_ticket_data(
    method: typing.Callable[[list[src.typings.FlightTicket], str], None],
    flight_ticket_data: src.typings.FlightTicket,
    file_name: str,
    new_header: str,
    new_column_value: str,
    tmp_path: pathlib.Path,
) -> None:
    """Assert method outputs valid flight ticket data correctly."""
    full_path = tmp_path / file_name
    method([], str(full_path))
    flight_ticket_data[new_header] = new_column_value
    assert not os.path.exists(f"{file_name}_1.csv")
    method([flight_ticket_data], str(full_path))
    assert os.path.exists(f"{full_path}_1.csv")
    method([flight_ticket_data], str(full_path))
    assert os.path.exists(f"{full_path}_2.csv")
    with open(f"{full_path}_1.csv", "r") as file:
        headers = file.readline().strip()
    assert headers == f"{BASE_OUTPUT_HEADERS},{new_header}"
