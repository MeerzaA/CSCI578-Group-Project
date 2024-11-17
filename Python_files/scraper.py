import os
from datetime import datetime, timedelta
from typing import Dict, List
import json

sources = ["source1", "source2", "source3"]

# Define the folder to store the results
RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), "../scrape_results/")

def ensure_results_folder():
    """
    Ensures that the results folder exists.
    """
    if not os.path.exists(RESULTS_FOLDER):
        os.makedirs(RESULTS_FOLDER)

def collect_and_combine_news(date: str):
    """
    Collects and combines news data from multiple sources into a single JSON file.

    :param date: Date to scrape news data
    """
    combined_data = {}

    for source in sources:
        # Fetch data for each source
        data = fetch_news_data(source, date)

        # Merge the news data from all sources
        combined_data.update(data)

    # Write the combined data to the output JSON file
    output_file = os.path.join(RESULTS_FOLDER, f"{date}.json")
    with open(output_file, "w") as file:
        json.dump(combined_data, file, indent=4)

def fetch_news_data(source: str, date: str) -> Dict[str, List[str]]:
    """
    Fetches news data from a given source for a specified day.

    :param source: Name of the news source
    :param date: Date to scrape news data
    """
    data = {}

    if source == "source1":
        # Fetch data from source1
        data = {"source1": [f"News from {source} on {date}"]}
    elif source == "source2":
        # Fetch data from source2
        data = {"source2": [f"News from {source} on {date}"]}
    elif source == "source3":
        # Fetch data from source3
        data = {"source3": [f"News from {source} on {date}"]}

    return data

def main():
    """
    Main function to check and create JSON files for the past 7 days if they do not already exist.
    """
    # Ensure the results folder exists
    ensure_results_folder()

    today = datetime.now()
    for i in range(7):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        output_file = os.path.join(RESULTS_FOLDER, f"{date}.json")
        
        if not os.path.exists(output_file):
            print(f"Generating news file for {date}...")
            collect_and_combine_news(date)
        else:
            print(f"News file for {date} already exists.")

if __name__ == "__main__":
    main()
