import requests

from .config import SOURCE_URL, TIMEOUT, START_DATE_T, END_DATE_T
from .models import DailyRate


class SourceError(Exception):
    """Raised when the exchange rates cannot be downloaded or read."""


class RateSource:
    """Downloads exchange rates from the API and returns DailyRate objects."""

    def __init__(self, url=SOURCE_URL, timeout=TIMEOUT,
                 start_date_t=START_DATE_T, end_date_t=END_DATE_T):
        self.url = url
        self.timeout = timeout
        self.start_date_t = start_date_t
        self.end_date_t = end_date_t

    def fetch_raw(self):
        """Download the JSON response."""
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as error:
            raise SourceError(str(error))

    def build_records(self, raw):
        """Turn the raw JSON into a list of DailyRate objects."""
        try:
            rates = raw["rates"]
        except (KeyError, TypeError):
            raise SourceError("unexpected response format")
        return [DailyRate(day, values) for day, values in rates.items()]

    def filter_records(self, records):
        """Keep only records whose date is inside the period."""
        return [
            r for r in records
            if r.date is not None and self.start_date_t <= r.date <= self.end_date_t
        ]

    def fetch(self):
        """Download, build and filter the records."""
        raw = self.fetch_raw()
        records = self.build_records(raw)
        return self.filter_records(records)