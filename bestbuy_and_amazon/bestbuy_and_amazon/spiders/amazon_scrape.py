# import scrapy


# class AmazonSpider(scrapy.Spider):
#     name = "amazon"
#     # allowed_domains = ["amazon.com"]

#     # Limit crawling to 4 pages
#     custom_settings = {"DEPTH_LIMIT": 1, "ROBOTSTXT_OBEY": False}

#     def start_requests(self):
#         items = ["laptops"]

#         for item in items:
#             search = f"https://www.amazon.com/s?k={item}&page=1"

#             yield scrapy.Request(search, self.parse, meta={"category": item})

#     # Parse webpages from Amazon
#     def parse(self, response):
#         amazon_items = response.css('div.s-search-results div[role="listitem"]')

#         # Cycle through items in result list
#         for item in amazon_items:
#             name = item.css(
#                 "div[data-cy='title-recipe'] a.a-link-normal.a-text-normal h2.a-color-base.a-text-normal span::text"
#             ).get()

#             item_category = response.meta.get("category")

#             item_url = (
#                 (
#                     "https://www.amazon.com"
#                     + item.css(
#                         "div[data-cy='title-recipe'] a.a-link-normal.a-text-normal::attr(href)"
#                     ).get()
#                 )
#                 if item.css(
#                     "div[data-cy='title-recipe'] a.a-link-normal.a-text-normal::attr(href)"
#                 ).get()
#                 != None
#                 else "No url"
#             )

#             price = round(
#                 float(
#                     item.css(
#                         'div[data-cy="price-recipe"] span[data-a-color="base"] span.a-offscreen::text'
#                     )
#                     .get()
#                     .replace("$", "")
#                     .replace(",", "")
#                 ),
#                 2,
#             )

#             original_price = (
#                 0
#                 if item.css(
#                     'div[data-cy="price-recipe"] div.a-section span.a-price span.a-offscreen::text'
#                 ).get()
#                 == None
#                 else round(
#                     float(
#                         item.css(
#                             'div[data-cy="price-recipe"] div.a-section span.a-price span.a-offscreen::text'
#                         )
#                         .get()
#                         .replace("$", "")
#                         .replace(",", "")
#                     ),
#                     2,
#                 )
#             )

#             if name == None or price == None:
#                 break

#             discount_percentage = (
#                 round(
#                     (original_price - price) / original_price * 100,
#                     2,
#                 )
#                 if original_price != 0
#                 else 0
#             )

#             starting_columns = {
#                 "name": name,
#                 "category": item_category,
#                 "price": price,
#                 "original_price": original_price,
#                 "discount_percentage": discount_percentage,
#             }

#             if item_category == "laptops":

#                 yield response.follow(
#                     item_url,
#                     callback=self.parse_laptop_page,
#                     meta={**starting_columns},
#                 )

#             # else:

#             #     yield {
#             #         "Category": item_category,
#             #         "Name": name,
#             #         "Price after Discount ($)": (price if original_price != 0 else 0),
#             #         "Original Price ($)": (
#             #             price if original_price == 0 else original_price
#             #         ),
#             #         "Discount Percentage": discount_percentage,
#             #         "Item URL": item_url,
#             #     }

#         for next_page in response.css("a.s-pagination-next ::attr(href)"):
#             yield response.follow(next_page, callback=self.parse)

#     def parse_laptop_page(self, response):

#         table = response.css("div.a-section table.a-normal tr")

#         brand = table.css("tr.po-brand span.po-break-word::text").get()

#         screen_size = (
#             table.xpath(
#                 "//tr[contains(@class,'po-display.size')]//span[contains(@class,'po-break-word')]//text()"
#             )
#             .get()
#             .split(" ")[0]
#         )

#         hdd_size = (
#             table.xpath(
#                 "//tr[contains(@class,'po-hard_disk.size')]//span[contains(@class,'po-break-word')]//text()"
#             )
#             .get()
#             .split(" ")
#         )

#         cpu_model = table.xpath(
#             "//tr[contains(@class,'po-cpu_model.family')]//span[contains(@class,'po-break-word')]//text()"
#         ).get()

#         ram = (
#             table.xpath(
#                 "//tr[contains(@class,'po-ram_memory.installed_size')]//span[contains(@class,'po-break-word')]//text()"
#             )
#             .get()
#             .split(" ")[0]
#         )

#         yield {
#             "Category": response.meta.get("category"),
#             "Name": response.meta.get("name"),
#             "Price after Discount ($)": (
#                 response.meta.get("price")
#                 if response.meta.get("original_price") != 0
#                 else 0
#             ),
#             "Original Price ($)": (
#                 response.meta.get("price")
#                 if response.meta.get("original_price") == 0
#                 else response.meta.get("original_price")
#             ),
#             "Discount Percentage": response.meta.get("discount_percentage"),
#             "Brand": brand,
#             "Screen Size (in)": screen_size,
#             "Hard Disk Size (GB)": (
#                 int(float(hdd_size[0]) * 1000) if hdd_size[1] == "TB" else hdd_size[0]
#             ),
#             "CPU Model": cpu_model,
#             "RAM (GB)": ram,
#             "Item URL": response.url,
#         }
