import scrapy
import os
import json
import datetime

class BInsiderSpider(scrapy.Spider):
    name = "BInsiderSpider"
    allowed_domains = ["businessinsider.com"]
    start_urls = ["https://www.businessinsider.com/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scraped_data = {}
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")

    def parse(self, response):
        titles = response.css('a.tout-title-link::text').getall()
        urls = response.css('a.tout-title-link::attr(href)').getall()

        for title, url in zip(titles, urls):
            full_url = response.urljoin(url)

            if "businessinsider" not in self.scraped_data:
                self.scraped_data["businessinsider"] = {"cryptocurrencies": {}}
            if "Bitcoin" not in self.scraped_data["businessinsider"]["cryptocurrencies"]:
                self.scraped_data["businessinsider"]["cryptocurrencies"]["Bitcoin"] = []

            self.scraped_data["businessinsider"]["cryptocurrencies"]["Bitcoin"].append({
                "title": title.strip(),
                "date": self.date,
                "url": full_url,
                "text": ""
            })

            yield response.follow(full_url, self.parse_details, meta={"article_url": full_url, "article_title": title.strip()})

    def parse_details(self, response):
        content = ' '.join(response.css('div.article-content p::text').getall()).strip()
        article_url = response.meta["article_url"]

        for article in self.scraped_data["businessinsider"]["cryptocurrencies"]["Bitcoin"]:
            if article["url"] == article_url:
                article["text"] = content if content else "No content available"
                break
            
            

    def closed(self, reason):
        # Set the output directory relative to the spider's directory
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
        output_file = os.path.join(output_dir, f"{self.date}.json")

        # Save the JSON file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.scraped_data, f, indent=4)

        self.log(f"Scraped data saved to {output_file}")

