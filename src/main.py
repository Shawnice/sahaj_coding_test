"""Main program."""

# Standard library
import argparse
import logging
import pathlib
import sys

logger = logging.getLogger(__name__)

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.absolute()))


# First-party
from src.flights import (get_flight_ticket_data,
                         output_invalid_flight_ticket_data,
                         output_valid_flight_ticket_data,
                         validate_flight_ticket_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=pathlib.Path)
    args = parser.parse_args()
    raw_flight_tickets = get_flight_ticket_data(args.file_name)
    valid_flight_ticket, invalid_flight_ticket = validate_flight_ticket_data(
        raw_flight_tickets
    )
    if valid_flight_ticket:
        output_file = output_valid_flight_ticket_data(valid_flight_ticket)
        logger.info(f"Generate valid flight ticket file: {output_file}")
    if invalid_flight_ticket:
        output_file = output_invalid_flight_ticket_data(invalid_flight_ticket)
        logger.info(f"Generate invalid flight ticket file: {output_file}")
