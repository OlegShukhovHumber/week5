from pathlib import Path

START_DATE = '2024-01-01'
END_DATE = '2024-06-30'

START_DATE_T = tuple(map(int, START_DATE.split("-")))   # (2024, 1, 1)
END_DATE_T = tuple(map(int, END_DATE.split("-")))       # (2024, 6, 30)

CURRENCIES = ["USD", "EUR", "GBP"]
BASE_CURRENCY = "CAD"

SOURCE_URL = (
    f"https://api.frankfurter.dev/v1/{START_DATE}..{END_DATE}"
    f"?from={BASE_CURRENCY}&to={','.join(CURRENCIES)}"
)
TIMEOUT = 10

OUTPUT_PATH = Path("data/processed/summary.json")