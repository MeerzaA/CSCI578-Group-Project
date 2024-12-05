import praw
from datetime import datetime, timedelta
import copy
import praw.models

MIN_COMMENTS = 1
MAX_COMMENTS = 20
DAY_RANGE = 30

class RedditCrawler:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id="f_pgbg_ASrz1R3OMw_mFbg",
            client_secret="fU4pc-GIkTgMFXLE6CHXu12eVSZmHg",
            user_agent="windows:CSCI578:v1.0.0 (by u/Account123456789)"
        )
        self.subreddit = self.reddit.subreddit("CryptoCurrency")
        self.CRYPTOCURRENCIES = (
            {
                'name': 'Ethereum',
                'search': 'ethereum',
                'symbol': 'ETH'
            },
            {
                'name': 'Bitcoin',
                'search': 'bitcoin btc',
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

    def collect_comments(self, search_results, search_name, lower_symbol, currency_name, send_callback, json_comments):
        """Collect comments and send them via a callback function."""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=DAY_RANGE)
        current_date = end_date

        num_comments = 0
        day_idx = 0
        searched = 0
        json_template = {
            "source_name": "reddit",
            "source_type": "social",
            "date": "",
            "cryptocurrency": "",
            "title": "",
            "url": "",
            "text": ""
        }
        for post in search_results:
            searched += 1
            # check post date
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

            if day_idx >= DAY_RANGE:
                print("dat index out of range")
                break

            if len(json_comments[day_idx]) == MAX_COMMENTS:
                continue

            json_template["title"] = post.title
            json_template["date"] = datetime.fromtimestamp(post.created_utc).strftime("%Y-%m-%d")
            json_template["url"] = post.url
            json_template["cryptocurrency"] = [currency_name]

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
                sent_data = {'Scraped_Format':[json_template]}
                send_callback(copy.deepcopy( sent_data))
                num_comments += 1

                if len(json_comments[day_idx]) == MAX_COMMENTS:
                    break

        return num_comments

    def crawl(self, send_callback):
        """Crawl Reddit and send results through the callback."""
        for currency in self.CRYPTOCURRENCIES:
            search_name = currency["search"].lower()
            lower_symbol = currency["symbol"].lower()
            currency_name = currency["name"]

            collected_comments = [[] for i in range(DAY_RANGE)]
            comment_count = self.collect_comments(
                self.subreddit.search(search_name, sort="new", time_filter="month", limit=None),
                search_name,
                lower_symbol,
                currency_name,
                send_callback,
                collected_comments
            )
            if comment_count < MIN_COMMENTS * DAY_RANGE and "sub" in currency:
                backup_sub = self.reddit.subreddit(currency["sub"])
                comment_count += self.collect_comments(
                    backup_sub.search(search_name, sort="new", time_filter="month", limit=None),
                    search_name,
                    lower_symbol,
                    currency_name,
                    send_callback,
                    collected_comments
                )

