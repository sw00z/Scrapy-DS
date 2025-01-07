# import scrapy


# class BestBuySpider(scrapy.Spider):
#     name = "bestbuy"
#     allowed_spaces = ["bestbuy.com"] 
#     custom_settings = {"DEPTH_LIMIT": 1, "ROBOTSTXT_OBEY": False}

#     def start_requests(self):
#         items = ["laptops", "headphones"]

#         for item in items:
#             search = f"https://www.bestbuy.com/site/searchpage.jsp?st={item}"

#             yield scrapy.Request(search, self.parse, meta={"category": item})

#     def parse(self, response):
#        bestbuy_items = response.css()