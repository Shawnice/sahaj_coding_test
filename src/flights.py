"""Module for handling flight ticket data."""

# Standard library
import csv
import logging
import os
import pathlib
import typing

# Third-party
import pydantic

# First-party
import src.models
import src.typings

logger = logging.getLogger(__name__)


def _increment_file_name(file_name: str) -> int:
    """Determine incremented file name."""
    i = 1
    while os.path.exists(f"{file_name}_{i}.csv"):
        i += 1
    return i


def _to_phone_number_model(phone_number: str) -> dict[str, str]:
    """Conform `Mobile_phone` to `PhoneNumber` schema."""
    return {"value": phone_number}


def _from_phone_number_model(phone_numer_model: dict[str, str]) -> str:
    """Covert `PhoneNumber` to `Mobile_phone` schema."""
    return phone_numer_model["value"]


def get_flight_ticket_data(
    file_name: pathlib.Path,
) -> list[src.typings.FlightTicket]:
    """Read flight ticket data from CSV file."""
    with file_name.open() as fin:
        raw_data = csv.reader(fin, delimiter=",")
        headers = [header.strip() for header in next(raw_data)]
        rows = [list(map(str.strip, row)) for row in raw_data]
    return [dict(zip(headers, row, strict=True)) for row in rows]


def output_valid_flight_ticket_data(
    flight_tickets: list[src.typings.FlightTicket],
    file_name: str = "./valid-flight-tickets",
) -> None:
    """Output valid flight ticket data to CSV file."""
    if not flight_tickets:
        return
    increment = _increment_file_name(file_name)
    with open(f"{file_name}_{increment}.csv", "w") as file:
        writer = csv.writer(file)
        for i, ticket in enumerate(flight_tickets):
            if i == 0:
                writer.writerow(ticket.keys())
            writer.writerow(ticket.values())


def output_invalid_flight_ticket_data(
    flight_tickets: list[src.typings.FlightTicket],
    file_name: str = "./invalid-flight-tickets",
) -> None:
    """Output invalid flight ticket data to CSV file."""
    if not flight_tickets:
        return
    increment = _increment_file_name(file_name)
    with open(f"{file_name}_{increment}.csv", "w") as file:
        writer = csv.writer(file)
        for i, ticket in enumerate(flight_tickets):
            if i == 0:
                writer.writerow(ticket.keys())
            writer.writerow(ticket.values())


def handle_errors(exc: pydantic.error_wrappers.ValidationError) -> str:
    """Handle model validation errors."""
    errors = []
    for error in exc.errors():
        if "PNR" in error["loc"]:
            errors.append("Invalid PNR")
        if "Mobile_phone" in error["loc"]:
            errors.append(error["msg"])
        if "Email" in error["loc"]:
            errors.append("Invalid email")
        if "Ticketing_date" in error["loc"]:
            errors.append(error["msg"])
        if "Booked_cabin" in error["loc"]:
            errors.append("Invalid Booked_cabin")
    return ",".join(errors)


def gen_discount_code(fare_class: str) -> str:
    """Generate a discount code based on `Fare_class`."""
    discount_code = ""
    if ord("A") <= ord(fare_class) <= ord("E"):
        discount_code = "OFFER_20"
    elif ord("F") <= ord(fare_class) <= ord("K"):
        discount_code = "OFFER_30"
    elif ord("L") <= ord(fare_class) <= ord("R"):
        discount_code = "OFFER_25"
    return discount_code

def validate_flight_ticket_data(
    flight_tickets: list[src.typings.FlightTicket],
) -> tuple[list[src.typings.FlightTicket], list[src.typings.FlightTicket]]:
    """Validate flight ticket data."""
    valid_flight_tickets = []
    invalid_flight_tickets = []
    for flight_ticket in flight_tickets:
        flight_ticket["Mobile_phone"] = _to_phone_number_model(
            str(flight_ticket["Mobile_phone"])
        )
        try:
            src.models.FlightTicket(**flight_ticket)  # type: ignore[arg-type]
            flight_ticket["Mobile_phone"] = _from_phone_number_model(
                typing.cast(dict[str, str], flight_ticket["Mobile_phone"])
            )
        except pydantic.ValidationError as exc:
            flight_ticket["Error"] = handle_errors(exc)
            invalid_flight_tickets.append(flight_ticket)
        else:
            flight_ticket["Discount_code"] = gen_discount_code(
                str(flight_ticket["Fare_class"])
            )
            valid_flight_tickets.append(flight_ticket)
        logger.debug(f"Processed flight ticket: {flight_ticket}")
    return valid_flight_tickets, invalid_flight_tickets
