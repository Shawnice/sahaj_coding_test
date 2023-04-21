# Sahaj Technical Test - Flight Ticket Validator

An application that validates input flight ticket data (CSV format) and
output valid and invalid flight ticket data into separate files.

## Installation

Run `make pip-install` to install dependencies. This will install packages from
all the requirement files under the project directory.

## Main program 

We create a script (src/main.py) that takes a CSV file as input and generates
one CSV file containing valid flight ticket data(if applicable) and the other
CSV file containing invalid flight ticket data(if applicable).

Run `python src/main.py <path-to-csv>`.

Ex: `python src/main.py tests/flight-ticket-data.csv`

Alternatively, you can also use make command to do it.

Ex: `make run FILE=tests/flight-ticket-data.csv`

**Note**: `tests/flight-ticket-data.csv` contains example valid and invalid
flight ticket data.

### Output CSV files

By default, valid flight ticket will be stored in
`./valid-flight-ticket_{index}.csv`, where index is an integer number. This
will ensure a new file is created whenever you execute the script.

In the valid flight ticket file, there will add one new column, `Discount_code`
, which is generated based on `Fare_class` value. For instance,

```csv
First_name,Last_name,PNR,Fare_class,Travel_date,Pax,Ticketing_date,Email,Mobile_phone,Booked_cabin,Discount_code
Abhishek,Kumar,ABC123,F,2019-07-31,2,2019-05-21,abhishek@zzz.com,7448212116,Economy,OFFER_30
```

Same as above, invalid flight ticket will be stored in 
`./invalid-flight-ticket_{index}.csv`.

In the invalid flight ticket file, there will add one new column, `Error`
, which is generated based on what errors occur during validation.
For instance,

```csv
First_name,Last_name,PNR,Fare_class,Travel_date,Pax,Ticketing_date,Email,Mobile_phone,Booked_cabin,Error
Monin,Sankar,PQ234,C,2019-08-30,2,2019-05-22,monin@zzz.com,{'value': '7448212117'},Economy,Invalid PNR
```

---

## Development

We provide a series of `make` utilities for development purposes. Run
`make help` for more information.

### Testing

Run test suites, execute `make test`. This will recursively check all tests
under this project.

### Format code

Format Python files with `isort` and `black`. Run `make format`.

### Linter

Run linters on Python files with `ruff` and `mypy`. Run `make lint`.

---

## Author

Lester Wu <wucean@gmail.com>
