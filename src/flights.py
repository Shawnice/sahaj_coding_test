# Standard library
import csv
import logging
import pathlib

# Third-party
import pydantic

# First-party
import src.models
import src.typings

logger = logging.getLogger(__name__)


def _to_phone_number_model(phone_number: str) -> dict[str, str]:
    """Conform `Mobile_phone` to `PhoneNumber` schema."""
    return {"value": phone_number}


def get_flight_ticket_data(
    file_name: pathlib.Path,
) -> list[src.typings.FlightTicket]:
    with file_name.open() as fin:
        raw_data = csv.reader(fin, delimiter=",")
        headers = [header.strip() for header in next(raw_data)]
        rows = [list(map(str.strip, row)) for row in raw_data]
    return [dict(zip(headers, row)) for row in rows]


def output_validated_flight_ticket_data(
    flight_tickets: list[src.typings.FlightTicket],
) -> None:
    with open("valid-flight-tickets.csv", "w") as file:
        writer = csv.writer(file)
        for i, ticket in enumerate(flight_tickets):
            if i == 0:
                writer.writerow(ticket.keys())
            writer.writerow(ticket.values())


def output_invalid_flight_ticket_data(
    flight_tickets: list[src.typings.FlightTicket],
) -> None:
    with open("invalid-flight-tickets.csv", "w") as file:
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
    if ord("A") <= ord(fare_class) <= ord("E"):
        return "OFFER_20"
    elif ord("F") <= ord(fare_class) <= ord("K"):
        return "OFFER_30"
    elif ord("L") <= ord(fare_class) <= ord("R"):
        return "OFFER_25"
    else:
        return ""


def process_flight_ticket_data(
    flight_tickets: list[src.typings.FlightTicket],
) -> None:
    validated_flight_tickets = []
    invalid_flight_tickets = []
    for flight_ticket in flight_tickets:
        flight_ticket["Mobile_phone"] = _to_phone_number_model(
            str(flight_ticket["Mobile_phone"])
        )
        try:
            src.models.FlightTicket(**flight_ticket)
        except pydantic.ValidationError as exc:
            flight_ticket["Error"] = handle_errors(exc)
            invalid_flight_tickets.append(flight_ticket)
        else:
            flight_ticket["Discount_code"] = gen_discount_code(
                str(flight_ticket["Fare_class"])
            )
            validated_flight_tickets.append(flight_ticket)
    output_validated_flight_ticket_data(validated_flight_tickets)
    output_invalid_flight_ticket_data(invalid_flight_tickets)
