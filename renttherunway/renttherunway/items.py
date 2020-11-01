# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RenttherunwayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()

    sub_name = scrapy.Field()

    rating = scrapy.Field()

    category = scrapy.Field()

    num_reviews = scrapy.Field()
    
    reviews = scrapy.Field()

