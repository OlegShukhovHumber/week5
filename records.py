import json
from pathlib import Path
import requests

start_date = '2024-01-01'
end_date = '2024-06-30'

start_date_t = (2024, 1, 1)
end_date_t = (2024, 6, 30)

SOURCE_URL = f"https://api.frankfurter.dev/v1/{start_date}..{end_date}?from=CAD&to=USD,EUR,GBP"
OUTPUT = Path(__file__).parent / "summary.json"



def fetch_rates(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    currency = response.json()

    return currency

data = fetch_rates(SOURCE_URL)

new_data = {}
for key in data['rates'].keys():
    new_data[tuple(map(int, key.split("-")))] = data['rates'][key]

def filter_rates(new_data):
    for key in list(new_data.keys()):
        if not start_date_t <= key <= end_date_t:
            del new_data[key]

    return new_data

filtered_data = filter_rates(new_data)

def calculate_monthly_average(filtered_data):
    months = {key[1] for key in filtered_data.keys()}
    filtered_data_by_month = {}

    avg_per_month = {}

    for month in months:
        usd_sum = 0
        eur_sum = 0
        gbp_sum = 0
        counter = 0

        filtered_data_by_month[month] = {}

        for key in filtered_data:
            if key[1] == month:
                usd_sum += filtered_data[key]['USD']
                eur_sum += filtered_data[key]['EUR']
                gbp_sum += filtered_data[key]['GBP']
                counter += 1

                filtered_data_by_month[month][key] = filtered_data[key]

        avg_per_month[month] = {
            'USD': usd_sum / counter,
            'EUR': eur_sum / counter,
            'GBP': gbp_sum / counter
        }

    return avg_per_month, filtered_data_by_month

def calculate_largest_change(filtered_data_by_month):
    big_dif_month = {}

    for month, data in filtered_data_by_month.items():
        dates = sorted(data.keys())

        max_change = {
            'USD': 0,
            'EUR': 0,
            'GBP': 0
        }

        for i in range(len(dates) - 1):
            current_day = dates[i]
            next_day = dates[i + 1]

            for currency in ['USD', 'EUR', 'GBP']:
                change = abs(
                    data[next_day][currency] - data[current_day][currency]
                )

                if change > max_change[currency]:
                    max_change[currency] = change

        big_dif_month[month] = max_change

    return big_dif_month


def build_summary(source_url, filtered_data, avg_per_month, largest_change):

    summary = {
        "source_url": source_url,
        "records_processed": len(filtered_data),
        "monthly_average": avg_per_month,
        "largest_daily_change": largest_change
    }

    return summary

def write_summary(summary, path):

    with path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2, ensure_ascii=False)

def main():

    data = fetch_rates(SOURCE_URL)

    new_data = {}

    for key in data['rates'].keys():
        new_data[tuple(map(int, key.split("-")))] = data['rates'][key]

    filtered_data = filter_rates(new_data)

    avg_per_month, filtered_data_by_month = calculate_monthly_average(filtered_data)

    largest_change = calculate_largest_change(filtered_data_by_month)

    summary = build_summary(
        SOURCE_URL,
        filtered_data,
        avg_per_month,
        largest_change
    )

    write_summary(summary, OUTPUT)

if __name__ == "__main__":
    main()