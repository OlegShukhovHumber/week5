from .config import CURRENCIES

class DailyRate:
    """Exchange rates for the base currency on a single day."""

    def __init__(self, day, rates):
        self.date = self._parse_date(day)                  # (2024, 1, 2) или None
        self.month = self.date[1] if self.date else None
        self.rates = {c: self._to_float(rates.get(c)) for c in CURRENCIES}

    def _parse_date(self, day):
        try:
            year, month, d = map(int, day.split("-"))
            return (year, month, d)
        except (ValueError, AttributeError):
            return None

    def _to_float(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def __str__(self):
        return f"{self.date}: " + ", ".join(f"{c}={v}" for c, v in self.rates.items())