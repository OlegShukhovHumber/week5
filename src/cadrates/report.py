import json


def build_summary(source_url, records, aggregations):
    """Build the summary dict by running every aggregation over the records."""
    summary = {
        "source_url": source_url,
        "records_processed": len(records),
    }
    for aggregation in aggregations:
        summary[aggregation.key] = aggregation.compute(records)
    return summary


def write_summary(summary, path):
    """Write the summary to a JSON file, creating the folder if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2, ensure_ascii=False)