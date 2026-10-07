# cadrates

Summarizes Canadian dollar (CAD) exchange rates against USD, EUR and GBP for January to June 2024: the monthly average and the largest daily change per month.

## Data source

Frankfurter API: https://api.frankfurter.dev/v1/2024-01-01..2024-06-30?from=CAD&to=USD,EUR,GBP

One record is one working day with the CAD rate for each of the three currencies. About 126 records.

## Setup

```
conda env create -f environment.yml
conda activate cadrates
pip install -r requirements.txt
pip install -e .
```

## Run

```
python main.py
```

The summary is written to `data/processed/summary.json`. If the download fails, the program prints one message and exits without a traceback.

## Test

```
python -m unittest discover -s tests
```

## Layout

- `src/cadrates/config.py`: dates, currencies, URL, timeout and output path, so all settings live in one place.
- `src/cadrates/models.py`: `DailyRate`, one clean record. It cleans its own values when it is created.
- `src/cadrates/sources.py`: `RateSource` downloads the data and builds records. It is the only module that imports `requests`.
- `src/cadrates/aggregations.py`: the `Aggregation` base class and its subclasses.
- `src/cadrates/report.py`: builds and writes the summary.
- `src/cadrates/__init__.py`: re-exports the public names.
- `main.py`: thin entry point that wires the pieces together and prints messages.
- `tests/`: unit tests with handmade records, no network.

## What moved where

| Lab 02 code | Where it lives now |
|---|---|
| constants (dates, URL, output path) | `config.py` |
| `fetch_rates` | `RateSource.fetch_raw` |
| `new_data` loop (date strings to tuples) | `DailyRate._parse_date` and `RateSource.build_records` |
| `filter_rates` | `RateSource.filter_records` |
| `calculate_monthly_average` | `MonthlyAverage.compute` |
| month grouping inside `calculate_monthly_average` | `Aggregation._group_by_month` |
| `calculate_largest_change` | `LargestDailyChange.compute` |
| `build_summary` | `report.build_summary` (loops over aggregation objects) |
| `write_summary` | `report.write_summary` |
| `main` | `main.main` (error handling and messages only) |

## Design choices

- `DailyRate` exists so that missing or malformed values are handled in one place, in `__init__`. The rest of the code does not check for bad data again.
- `RateSource` hides `requests` and turns every network problem into `SourceError`, so `main.py` does not need to know about `requests`.
- `Aggregation` is a base class that defines `compute(records)` and provides the shared `_group_by_month`. `MonthlyAverage` and `LargestDailyChange` override `compute`. `build_summary` calls `compute` on every object without checking its type. Adding a new statistic, for example a monthly minimum, means writing one subclass with a `key` and a `compute` method and adding it to the list in `main.py`.

## Known limitations

- Dates are stored as tuples such as (2024, 1, 2) instead of `datetime.date`.
- The period and currencies are fixed in `config.py`, with no command line options.
- Records with a bad date are dropped silently.
- The output path is relative, so the program must be run from the repository root.
- Tests cover only `DailyRate`.