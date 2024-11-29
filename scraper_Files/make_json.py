import os
from datetime import datetime, timedelta
from typing import Dict, List
import json

news_sources = ["nytimes", "wsj"]
social_media_sources = ["reddit"]

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

    for source in news_sources+social_media_sources:
        # Fetch data for each source
        source_data = fetch_news_data(source, date)

        # Detailing source type
        if source in news_sources:
            source_data["source_type"] = "news"
        elif source in social_media_sources:
            source_data["source_type"] = "social_media"

        # Merge the news data from all sources
        combined_data.update(source_data)


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
        # data[source]["cryptocurrencies"] = fetch_data_from_source1(date)- THIS IS HOW TO FETCH DATA FROM SOURCE
        
        # Fetch data from source1 - THIS IS FORMAT RETURNED BY SCRAPER FOR EACH SOURCE (fetch_data_from_source1)
        data[source]["cryptocurrencies"] = {
            "Bitcoin": [
                {
                    "title": "Bitcoin blah blah ",
                    "date": "2021-06-25",
                    "url": "https://www.nytimes.com/2021/06/25/technology/bitcoin-cryptocurrency.html",
                    "text": "good - i like bitcoin"
                },
                {
                    "title": "Bitcoin blah blah blah",
                    "date": "2021-06-25",
                    "url": "https://www.nytimes.com/2021/06/25/technology/bitcoin-cryptocurrency.html",
                    "text": "very good"
                }
            ],
            "Ethereum": [
                {
                    "title": "Ethereum blah blah",
                    "date": "2021-06-25",
                    "url": "https://www.nytimes.com/2021/06/25/technology/bitcoin-cryptocurrency.html",
                    "text": "i love ethereum"
                },
                {
                    "title": "Ethereum blah blah",
                    "date": "2021-06-25",
                    "url": "https://www.nytimes.com/2021/06/25/technology/bitcoin-cryptocurrency.html",
                    "text": "ethereum is all right, i like bitcoin more"
                }
            ]
        }
    # elif source == "source2":
    #     # Fetch data from source2
    #      data[source]["cryptocurrencies"] = {}
    # elif source == "source3":
    #     # Fetch data from source3
    #     data[source]["cryptocurrencies"] = {}


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
