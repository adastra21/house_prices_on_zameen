import scrapy
import json
from datetime import datetime

class ZameenSpider(scrapy.Spider):
    name = "zameen"

    def start_requests(self):
        start_urls = [
            "https://www.zameen.com/Homes/Lahore-1-1.html",
            "https://www.zameen.com/Rentals/Lahore-1-1.html",
            "https://www.zameen.com/Plots/Lahore-1-1.html",
            "https://www.zameen.com/Commercial/Lahore-1-1.html",
            "https://www.zameen.com/Homes/Karachi-2-1.html",
            "https://www.zameen.com/Rentals/Karachi-2-1.html",
            "https://www.zameen.com/Plots/Karachi-2-1.html",
            "https://www.zameen.com/Commercial/Karachi-2-1.html",
            "https://www.zameen.com/Homes/Islamabad-3-1.html",
            "https://www.zameen.com/Rentals/Islamabad-3-1.html",
            "https://www.zameen.com/Plots/Islamabad-3-1.html",
            "https://www.zameen.com/Commercial/Islamabad-3-1.html",
        ]
        for url in start_urls:
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta["start_url"] = url
            request.meta["page_number"] = 1
            yield request

    def parse(self, response):
        PROPERTY_XPATH = "//*[@class='_7ac32433']/@href"

        for r in response.xpath(PROPERTY_XPATH):
            href = r.get()
            yield scrapy.Request(url=response.urljoin(href), 
                callback=self.parse_property)

        page_number = str(int(response.meta["page_number"]) + 1)
        start_url = response.meta["start_url"]
        new_url = start_url[0:-6] + page_number + ".html"
        request = scrapy.Request(url=new_url, callback=self.parse)
        request.meta["start_url"] = start_url
        request.meta["page_number"] = page_number
        yield request

    def parse_property(self, response):
        property_id = "//span[@class='c5051fb4']//text()"
        # title, subtitle
        titles = "//*[@class='b72558b0']"
        # type, price, location, beds, baths, area, purpose, added
        details = "//ul[@class='_033281ab']/li//text()"
        # age, floors, servant quarters, other features
        amenities = "//*[@class='_17984a2c']/text()"
        # free-form text field
        description = "//*[@class='_2a806e1e']/text()"
        # agency name, agent, titanium
        agency_name = "//div[@class='_5a588edf']/text()"
        agent = "//span[@class='_725b3e64']/text()"
        titanium = "//div[@class='f79dd41f']//text()"
        # agency video
        agency_video = "//div[@class='_220d9e63']"
        # count of images, tour video, verified
        images = "//div[@class='_37beb648 _931ce63f']/text()"
        tour_video = "//div[contains(@class, 'ed8e3fc8')]/text()"
        verified = "//span[contains(@class, 'dba0affc')]/text()"
        # price estimates
        # current_price = "//li[@class='_4a87fc54']/*/text()"
        # price_change = "//li[@class='_100d11ec']/*/text()"

        # last string of page breadcrumb
        PROPERTY_ID = response.xpath(property_id).getall()[-1]

        for r in response.xpath(titles):
            TITLE = r.xpath("./h1/text()").get()
            SUBTITLE = r.xpath("./div/text()").get()
        
        DETAILS = response.xpath(details).getall()
        DESCRIPTION = " ".join(response.xpath(description).getall())
        AMENITIES = " ".join(response.xpath(amenities).getall())
        AGENCY = response.xpath(agency_name).get()
        AGENT = response.xpath(agent).get()

        if response.xpath(titanium).get():
            TITANIUM = True
        else:
            TITANIUM = False

        agency_video_exists = response.xpath(agency_video).getall()
        if len(agency_video_exists) > 0:
            AGENCY_VIDEO = True
        else:
            AGENCY_VIDEO = False

        count_of_images = response.xpath(images).get()
        if count_of_images:
            IMAGES = int(count_of_images)
        else:
            IMAGES = 0

        if len(response.xpath(tour_video).getall()) > 0:
            TOUR_VIDEO = True
        else:
            TOUR_VIDEO = False

        if len(response.xpath(verified).getall()) > 0:
            VERIFIED = True
        else:
            VERIFIED = False

        # PRICE_ESTIMATE = response.xpath(current_price).getall()
        # PRICE_ESTIMATE_CHANGE = response.xpath(price_change).getall()

        TODAYS_DATE = datetime.today().strftime("%m-%d-%Y, %H:%M:%S")
        DATESTAMP = datetime.today().strftime("%m-%d-%Y")

        PROPERTY_URL = response.url

        propinfo = {"Property ID": PROPERTY_ID,
                    "Title": TITLE,
                    "Subtitle": SUBTITLE,
                    "Details": DETAILS,
                    "Description": DESCRIPTION,
                    "Amenities": AMENITIES,
                    "Agency": AGENCY,
                    "Agent": AGENT,
                    "Titanium Agency?": TITANIUM,
                    "Agency Video": AGENCY_VIDEO,
                    "Number of Images": IMAGES,
                    "Tour Video": TOUR_VIDEO,
                    "Property Verified": VERIFIED,
                    # "Price Estimate": PRICE_ESTIMATE,
                    # "Price Estimate Change": PRICE_ESTIMATE_CHANGE,
                    "Date Scraped": TODAYS_DATE,
                    "URL": PROPERTY_URL}

        # print("##################################################################################")
        # print(propinfo)
        # print("##################################################################################")

        filename = "zameen_"+DATESTAMP+".json"
        path = filename

        try:
            with open(path, "a+") as outfile:
                json.dump(propinfo, outfile)
        except Exception as e: print(e)
