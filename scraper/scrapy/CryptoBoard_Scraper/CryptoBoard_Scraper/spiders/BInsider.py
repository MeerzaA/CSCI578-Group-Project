import scrapy
from datetime import datetime


class BinsiderspriderSpider(scrapy.Spider):
    name = "BInsiderSpider"
    allowed_domains = ["businessinsider.com"]
    start_urls = ["https://www.businessinsider.com/"]

    # Initialize an empty dictionary to hold the scraped data
    scraped_data = {"businessinsider": {}}

    def parse(self, response):
        # Extract article titles and links
        Tout_Titles = response.css('h3.tout-title')
        
        for title in Tout_Titles:
            article_title = title.css('a.tout-title-link::text').get()
            relative_url = title.css('a.tout-title-link::attr(href)').get()
            
            if article_title and relative_url:  # Ensure both title and URL exist
                full_url = response.urljoin(relative_url)
                yield response.follow(
                    full_url,
                    self.parse_details,
                    meta={"article_title": article_title.strip()}
                )

    def parse_details(self, response):
        # Extract article content
        article_title = response.meta.get("article_title", "No Title")
        content = ' '.join(response.css('div.article-content p::text').getall())
        date = response.css('time::attr(datetime)').get()  # Adjust selector for date
        category = "Bitcoin" if "bitcoin" in article_title.lower() else "Other"

        # Fallback for missing date
        date = date or datetime.now().strftime("%Y-%m-%d")

        # Prepare the article data
        article_data = {
            "title": article_title,
            "date": date,
            "url": response.url,
            "text": content.strip() if content else "No content available",
        }

        # Add to the scraped_data dictionary
        if category not in self.scraped_data["businessinsider"]:
            self.scraped_data["businessinsider"][category] = []
        
        self.scraped_data["businessinsider"][category].append(article_data)

    def closed(self, reason):
        # The spider is finished; print or save the dictionary
        self.log("Scraping completed. Here's the dictionary:")
        self.log(self.scraped_data)

        # Optional: Save the dictionary to a JSON file
        import json
        with open("scraped_data.json", "w") as f:
            json.dump(self.scraped_data, f, indent=4)
