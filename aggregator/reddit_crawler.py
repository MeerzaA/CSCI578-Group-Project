import praw
import datetime
import copy
import praw.models

MIN_COMMENTS = 20

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
            }
        )

    def collect_comments(self, search_results, search_name, lower_symbol, currency_name, send_callback):
        """Collect comments and send them via a callback function."""
        num_comments = 0
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
            lower_title = post.title.lower()
            if not (lower_symbol in lower_title or search_name in lower_title):
                continue

            json_template["title"] = post.title
            json_template["date"] = datetime.datetime.fromtimestamp(post.created_utc).strftime("%Y-%m-%d")
            json_template["url"] = post.url
            json_template["cryptocurrency"] = [currency_name]

            for comment in post.comments:
                if type(comment) is not praw.models.Comment:
                    continue

                if comment.author and comment.author.name.lower() == "automoderator":
                    continue

                lower_body = comment.body.lower()
                if not (lower_symbol in lower_body or search_name in lower_body):
                    continue

                json_template["text"] = comment.body
                send_callback(copy.deepcopy(json_template))
                num_comments += 1
        return num_comments

    def crawl(self, send_callback):
        """Crawl Reddit and send results through the callback."""
        for currency in self.CRYPTOCURRENCIES:
            search_name = currency["search"].lower()
            lower_symbol = currency["symbol"].lower()
            currency_name = currency["name"]

            comment_count = self.collect_comments(
                self.subreddit.search(search_name, sort="new", time_filter="week"),
                search_name,
                lower_symbol,
                currency_name,
                send_callback
            )
            if comment_count < MIN_COMMENTS and "sub" in currency:
                backup_sub = self.reddit.subreddit(currency["sub"])
                comment_count += self.collect_comments(
                    backup_sub.top(time_filter="week"),
                    search_name,
                    lower_symbol,
                    currency_name,
                    send_callback
                )

            print(f"{comment_count} comments recorded for {currency_name}")
