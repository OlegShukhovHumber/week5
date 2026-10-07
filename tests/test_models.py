import unittest

from cadrates import DailyRate


class TestDailyRate(unittest.TestCase):

    def test_normal_record(self):
        record = DailyRate("2024-01-02", {"USD": 0.75, "EUR": 0.69, "GBP": 0.59})
        self.assertEqual(record.date, (2024, 1, 2))
        self.assertEqual(record.month, 1)

    def test_missing_currency(self):
        record = DailyRate("2024-01-02", {"USD": 0.75, "EUR": 0.69})
        self.assertIsNone(record.rates["GBP"])

    def test_bad_date(self):
        record = DailyRate("not-a-date", {"USD": 0.75, "EUR": 0.69, "GBP": 0.59})
        self.assertIsNone(record.date)


if __name__ == "__main__":
    unittest.main()