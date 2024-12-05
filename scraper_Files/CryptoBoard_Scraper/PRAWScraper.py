import praw
import praw.models
import os
import json
import datetime
import copy

OUTPUT_DIR = "../scrape_results"
MIN_COMMENTS = 20

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
        'name': 'XRP',
        'search': 'xrp',
        'symbol': 'XRP',
        'sub': 'xrp'
    },
    {
        'name': 'TetherUS',
        'search': 'tether',
        'symbol': 'USDT'
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
        'name': 'USD Coin',
        'search': 'usdc',
        'symbol': 'USDC',
        'sub': 'usdc'
    },
    {
        'name': 'Avalanche',
        'search': 'avalanche',
        'symbol': 'AVAX',
        'sub': 'Avax'
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


def collect_comments(search_results):
    num_comments = 0
    for post in search_results:

        # only consider titles directly mentioning the currency
        lower_title = post.title.lower()
        if not (lower_symbol in lower_title or search_name in lower_title):
            continue

        json_template["title"] = post.title
        json_template["date"] = datetime.datetime.fromtimestamp(post.created_utc).strftime("%Y-%m-%d")
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
            scraped_data["Scraped_Format"].append(copy.deepcopy(json_template))
            num_comments += 1
    return num_comments


#collect comments for all cryptos
for currency in CRYPTOCURRENCIES:
    search_name = currency["search"].lower()
    lower_symbol = currency["symbol"].lower()
    currency_name = currency["name"]
    json_template["cryptocurrency"] = [currency_name]

    # record at least 20 comments, if not search the specific subreddit
    comment_count = collect_comments(subreddit.search(search_name, sort="new", time_filter="week"))
    if comment_count < MIN_COMMENTS and "sub" in currency.keys():
        backup_sub = reddit.subreddit(currency["sub"])
        comment_count += collect_comments(backup_sub.top(time_filter="week"))

    print(f"{comment_count} comments recorded for {currency_name}")

# Set the output directory relative to the spider's directory
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), OUTPUT_DIR))
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
date = datetime.datetime.now().strftime("%Y-%m-%d")
output_file = os.path.join(output_dir, f"reddit-{date}.json")

# Save the JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(scraped_data, f, indent=4)

print(f"Scraped data saved to {output_file}")
