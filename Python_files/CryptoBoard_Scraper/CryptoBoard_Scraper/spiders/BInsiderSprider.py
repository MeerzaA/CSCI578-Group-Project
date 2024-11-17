import scrapy

class BinsiderspriderSpider(scrapy.Spider):
    
    name = "BInsiderSprider"
    
    allowed_domains = ["www.businessinsider.com"]
    
    start_urls = [
        
        "https://www.businessinsider.com/"
    ]

    def parse(self, response):
        
        base_url = 'https://www.businessinsider.com'
        Tout_Titles = response.css('h3.tout-title')
        
        for title in Tout_Titles:
            name = title.css('a.tout-title-link::text').get() 
            relative_url = title.css('a.tout-title-link::attr(href)').get() 
            full_url = base_url + relative_url
            
            yield {
                'name': name, 
                'url': full_url
            }
           
            yield response.follow(full_url, self.parse_details)

    def parse_details(self, response):
      
        content = response.css('div.article-content::text').get()
        yield {
            'content': content
        }

import scrapy

