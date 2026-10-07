import sys

from cadrates import (
    RateSource,
    SourceError,
    MonthlyAverage,
    LargestDailyChange,
)
from cadrates.config import SOURCE_URL, OUTPUT_PATH
from cadrates.report import build_summary, write_summary


def main():
    try:
        records = RateSource().fetch()
    except SourceError as error:
        print(f"Could not download exchange rates: {error}")
        sys.exit(1)

    aggregations = [MonthlyAverage(), LargestDailyChange()]
    summary = build_summary(SOURCE_URL, records, aggregations)
    write_summary(summary, OUTPUT_PATH)

    print(f"Processed {len(records)} records.")
    print(f"Summary written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()