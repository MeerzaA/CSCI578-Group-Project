import praw
import praw.models
import os
import json
import datetime
import copy

reddit = praw.Reddit(
    client_id="f_pgbg_ASrz1R3OMw_mFbg",
    client_secret="fU4pc-GIkTgMFXLE6CHXu12eVSZmHg",
    user_agent="windows:CSCI578:v1.0.0 (by u/Account123456789)",
)

subreddit = reddit.subreddit("CryptoCurrency")

cryptocurrencies = (
    {
        'name': 'Ethereum',
        'symbol': 'ETH'
    },
    {
        'name': 'Bitcoin',
        'symbol': 'BTC'
    })

scraped_data = {"Scraped_Format": []}
json_template = {
    "source_name": "reddit",
    "source_type": "social",
    "date": "",
    "cryptocurrency": "",
    "title": "",
    "url": "",
    "text": ""
}

for currency in cryptocurrencies:
    lower_name = currency["name"].lower()
    lower_symbol = currency["symbol"].lower()

    json_template["cryptocurrency"] = [currency["name"]]

    for post in subreddit.search(lower_name, sort="new", time_filter="week"):

        # only consider titles directly mentioning the currency
        lower_title = post.title.lower()
        if not (lower_symbol in lower_title or lower_name in lower_title):
            continue

        json_template["title"] = post.title
        json_template["date"] = datetime.datetime.fromtimestamp(post.created_utc).strftime("%Y-%m-%d")
        json_template["url"] = post.url

        for comment in post.comments:
            if type(comment) is not praw.models.Comment:
                continue

            # only consider posts directly mentioning the currency
            lower_body = comment.body.lower()
            if not (lower_symbol in lower_body or lower_name in lower_body):
                continue

            json_template["text"] = comment.body
            scraped_data["Scraped_Format"].append(copy.deepcopy(json_template))

# Set the output directory relative to the spider's directory
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../scrape_results"))
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
date = datetime.datetime.now().strftime("%Y-%m-%d")
output_file = os.path.join(output_dir, f"reddit-{date}.json")

# Save the JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(scraped_data, f, indent=4)

print(f"Scraped data saved to {output_file}")