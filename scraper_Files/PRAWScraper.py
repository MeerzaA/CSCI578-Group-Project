import praw
import praw.models
import os
import json
from datetime import datetime, timedelta
import copy

OUTPUT_DIR = "../scrape_results"
MIN_COMMENTS = 1
MAX_COMMENTS = 20
DAY_RANGE = 30

reddit = praw.Reddit(
    client_id="f_pgbg_ASrz1R3OMw_mFbg",
    client_secret="fU4pc-GIkTgMFXLE6CHXu12eVSZmHg",
    user_agent="windows:CSCI578:v1.0.0 (by u/Account123456789)",
)

subreddit = reddit.subreddit("CryptoCurrency")

CRYPTOCURRENCIES = (
    {
        'name': 'Ethereum',
        'search': 'ethereum',
        'symbol': 'ETH'
    },
    {
        'name': 'Bitcoin',
        'search': 'bitcoin',
        'symbol': 'BTC'
    },
    {
        'name': 'Ripple',
        'search': 'xrp',
        'symbol': 'XRP',
        'sub': 'xrp'
    },
    {
        'name': 'Solana',
        'search': 'solana',
        'symbol': 'SOL ',
        'sub': 'solana'
    },
    {
        'name': 'BNB',
        'search': 'bnb',
        'symbol': 'BNB',
        'sub': 'bnbchainofficial'
    },
    {
        'name': 'Dogecoin',
        'search': 'dogecoin',
        'symbol': 'DOGE',
        'sub': 'dogecoin'
    },
    {
        'name': 'Cardano',
        'search': 'cardano',
        'symbol': 'ADA',
        'sub': 'cardano'
    },
    {
        'name': 'Avalanche',
        'search': 'avalanche',
        'symbol': 'AVAX',
        'sub': 'Avax'
    },
    {
        'name': 'Litecoin',
        'search': 'ltc',
        'symbol': 'LTC',
        'sub': 'litecoin'
    },
    {
        'name': 'Shiba Inu',
        'search': 'shib',
        'symbol': 'SHIB',
        'sub': 'Shibainucoin'
    })

test = (
    {
        'name': 'Shiba Inu',
        'search': 'shib',
        'symbol': 'SHIB',
        'sub': 'Shibainucoin'
    },
)

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


def collect_comments(search_results, json_comments):
    # Get today's date in UTC and calculate the start date (1 year ago)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=DAY_RANGE)
    current_date = end_date

    num_comments = 0
    day_idx = 0
    searched = 0
    for post in search_results:
        searched += 1
        #check post date
        start_time = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(days=1) - timedelta(microseconds=1)
        post_time = datetime.fromtimestamp(post.created_utc)
        if post_time <= start_date:
            print("post date out of range")
            break

        if post_time >= end_time:
            continue

        # only consider titles directly mentioning the currency
        lower_title = post.title.lower()
        if not (lower_symbol in lower_title or search_name in lower_title):
            continue

        while post_time <= start_time:
            current_date -= timedelta(days=1)
            start_time = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_time = start_time + timedelta(days=1) - timedelta(microseconds=1)
            day_idx += 1
            # print(f"now on day {day_idx}")

        if day_idx >= DAY_RANGE:
            print("dat index out of range")
            break

        if len(json_comments[day_idx]) == MAX_COMMENTS:
            continue

        json_template["title"] = post.title
        json_template["date"] = post_time.strftime("%Y-%m-%d")
        json_template["url"] = post.url

        for comment in post.comments:
            if type(comment) is not praw.models.Comment:
                continue

            if comment.author and comment.author.name.lower() == "automoderator":
                continue

            # only consider posts directly mentioning the currency
            lower_body = comment.body.lower()
            if not (lower_symbol in lower_body or search_name in lower_body):
                continue

            json_template["text"] = comment.body
            json_comments[day_idx].append(copy.deepcopy(json_template))
            num_comments += 1

            # if len(json_comments[day_idx]) == MIN_COMMENTS:
                # print(f"min comments reached for day {day_idx}")

            if len(json_comments[day_idx]) == MAX_COMMENTS:
                # print(f"max comments reached for day {day_idx}")
                break

    print(f"{day_idx} days searched, {searched} posts")
    return num_comments


#collect comments for all cryptos
for currency in test:
    search_name = currency["search"].lower()
    lower_symbol = currency["symbol"].lower()
    currency_name = currency["name"]
    json_template["cryptocurrency"] = [currency_name]

    # record at least min comments per day, if not search the specific subreddit
    collected_comments = [[] for i in range(DAY_RANGE)]

    comment_count = collect_comments(subreddit.search(search_name, sort="new", time_filter="month", limit=None), collected_comments)
    if comment_count < MIN_COMMENTS * DAY_RANGE and "sub" in currency.keys():
        backup_sub = reddit.subreddit(currency["sub"])
        comment_count += collect_comments(backup_sub.search(search_name, sort="new", time_filter="month", limit=None), collected_comments)

    d = 0
    for item in collected_comments:
        temp = 0
        for comment in item:
            scraped_data["Scraped_Format"].append(comment)
            temp += 1
        # print(f"{temp} comments for day {d}")
        d += 1

    print(f"{comment_count} comments recorded for {currency_name}")

# Set the output directory relative to the spider's directory
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), OUTPUT_DIR))
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
date = datetime.now().strftime("%Y-%m-%d")
output_file = os.path.join(output_dir, f"reddit-{date}.json")

# Save the JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(scraped_data, f, indent=4)

print(f"Scraped data saved to {output_file}")
