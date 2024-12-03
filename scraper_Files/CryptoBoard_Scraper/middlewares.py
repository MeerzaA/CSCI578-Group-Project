# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

import random
import time

class CryptoboardScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # Scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider,
        # after it has processed the response.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # raises an exception.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class RotateUserAgentMiddleware:
    # Middleware for rotating user agents to avoid detection.
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
    ]

    def process_request(self, request, spider):
        # Assigns a random user agent to each request.
        user_agent = random.choice(self.USER_AGENTS)
        request.headers['User-Agent'] = user_agent
        spider.logger.info(f'Using User-Agent: {user_agent}')

class RetryOn429Middleware:
    # Middleware for retrying requests that return HTTP 429.
    def process_response(self, request, response, spider):
        if response.status == 429:
            # Retry the request if server responds with 429 Too Many Requests.
            spider.logger.warning(f"429 Too Many Requests for {request.url}. Retrying...")
            return request
        return response

    def process_exception(self, request, exception, spider):
        # Log the exception and continue with other requests.
        spider.logger.error(f"Request failed for {request.url}: {exception}")
        return None


class DelayRequestsMiddleware:
    # Middleware for adding a delay between requests to mimic human behavior.
    def __init__(self, delay):
        self.delay = delay

    @classmethod
    def from_crawler(cls, crawler):
        # Retrieves the delay setting from Scrapy's settings.
        return cls(delay=crawler.settings.get('DOWNLOAD_DELAY', 1))

    def process_request(self, request, spider):
        # Introduces a delay before processing the request.
        time.sleep(self.delay)