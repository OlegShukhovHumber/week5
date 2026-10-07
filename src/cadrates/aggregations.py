from .config import CURRENCIES


class Aggregation:
    """Base class: one named statistic computed over a list of DailyRate."""

    key = None   # ключ в summary.json, задаётся в подклассах

    def compute(self, records):
        """Return the statistic. Every subclass must override this."""
        raise NotImplementedError

    def _group_by_month(self, records):
        """Return {month: [records of that month]}, skipping records without a date."""
        groups = {}
        for record in records:
            if record.month is None:
                continue
            if record.month not in groups:
                groups[record.month] = []
            groups[record.month].append(record)
        return groups


class MonthlyAverage(Aggregation):
    """Average rate of each currency per month."""

    key = "monthly_average"

    def compute(self, records):
        groups = self._group_by_month(records)
        result = {}
        for month in sorted(groups):
            result[month] = {}
            for currency in CURRENCIES:
                values = [r.rates[currency] for r in groups[month]
                          if r.rates[currency] is not None]
                result[month][currency] = sum(values) / len(values) if values else None
        return result


class LargestDailyChange(Aggregation):
    """Largest day-to-day change of each currency per month."""

    key = "largest_daily_change"

    def _get_date(self, record):
        return record.date

    def compute(self, records):
        groups = self._group_by_month(records)
        result = {}
        for month in sorted(groups):
            days = sorted(groups[month], key=self._get_date)
            max_change = {currency: 0 for currency in CURRENCIES}

            for i in range(len(days) - 1):
                today = days[i]
                tomorrow = days[i + 1]
                for currency in CURRENCIES:
                    before = today.rates[currency]
                    after = tomorrow.rates[currency]
                    if before is None or after is None:
                        continue
                    change = abs(after - before)
                    if change > max_change[currency]:
                        max_change[currency] = change

            result[month] = max_change
        return result