import scrapy
from datetime import datetime, timedelta


class BoyzSpider(scrapy.Spider):
    name = "boyznetweb"
    start_urls = ["https://netweb.netdatacorp.net/NDLEC/bok/cgibokcole.html"]
    response = "https://netweb.netdatacorp.net/NDLEC/bok/CGIBOK109.ws"
    date = str((datetime.now()-timedelta(days=7)).strftime("%m/%d/%Y"))

    def parse(self, response):
        input_data = {
            "S109ASOFDT": self.date,
            "S109INMNAM": "a",
        }

        yield scrapy.FormRequest.from_response(response, formdata=input_data, callback=self.parse2)

    def parse2(self, response):
        custom_settings = {
            'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter'
        }

        # yield {
        #     "date": response.css("H02-DATE::text").get(),
        # }

        for i in range (len(response.css("L01-KEY::text"))):
            inmates_data = {
                "S101KEY": response.css("L01-KEY::text")[i].get(),
                "S101LIB": "DATACOLE",
                "S101PFX": "LE",
                "S101CNTY": "Coleman",
                "S101COCOD": "COLEM",
            }
            yield scrapy.FormRequest(url="https://netweb.netdatacorp.net/NDLEC/bok/CGIBOK101.ws", formdata=inmates_data, callback=self.parse3)

        # for i in range (len(response.css("L01-KEY::text"))):
        #     yield{
        #         "js id": response.css("L01-KEY::text")[i].get(),
        #         "arrest number": response.css("L01-ARREST-NO::text")[i].get(),
        #         "inmate name": response.css("L01-INMATE-NAME::text")[i].get(),
        #         "book date": response.css("L01-BOOK-DATE::text")[i].get(),
        #         "charge": response.css("L01-CHARGE::text")[i].get(),
        #     }

        next_page = {
            "S109ORD": "NX",
            "109ASOFDT": self.date,
            "S109INMNAM": response.css("L01-INMATE-NAME::text")[-1].get(),
            "S109KEY": response.css("L01-KEY::text")[-1].get(),
            "S109LIB": "DATACOLE",
            "S109PFX": "LE",
            "S109CNTY": "Coleman",
            "S109COCOD": "COLEM",
            }

        yield scrapy.FormRequest(url="https://netweb.netdatacorp.net/NDLEC/bok/CGIBOK109.ws", formdata=next_page, callback=self.parse4)
    

    def parse3(self, response):
        # from scrapy.shell import inspect_response
        # from scrapy.utils.response import open_in_browser

        # open_in_browser(response)

        # inspect_response(response, self)
       
        yield{
            "pid": response.css("L02-ITEM1::text")[0].get().replace(" ",""),
            "arrest number": response.css("L02-ITEM1::text")[1].get().replace(" ",""),
            "name": response.css("L02-ITEM1::text")[2].get(),
            "alias": response.css("L02-ITEM1::text")[3:].getall(),
            "race": response.css("L04-ITEM1::text")[0].get().replace(" ",""),
            "ethnic": response.css("L04-ITEM2::text")[0].get(),
            "sex": response.css("L04-ITEM3::text")[0].get(),
            "age": response.css("L04-ITEM4::text")[0].get(),
            "dob": response.css("L04-ITEM5::text").get(),                
            "place of birth": response.css("L04-ITEM1::text")[1].get(),
            "height": response.css("L04-ITEM1::text")[2].get().replace("""\"""", """''"""),
            "weight": response.css("L04-ITEM2::text")[2].get(),
            "hair": response.css("L04-ITEM3::text")[2].get(),
            "eyes": response.css("L04-ITEM4::text")[2].get(),
            "glasses": response.css("L04-ITEM1::text")[3].get(),
            "facial hair": response.css("L04-ITEM2::text")[3].get(),
            "skin": response.css("L04-ITEM3::text")[3].get(),
            "scars/marks": response.css("L04-ITEM1::text")[4:-1].getall(),
            "build": response.css("L04-ITEM1::text")[-1].get(),
            "offense": response.css("L27-CHARGE::text").getall(),
            "bond amount": response.css("L27-BOND-AMT::text").getall(),
            "book date": response.css("L27-BOOKIN-DATE::text").getall(),
            "release date": response.css("L27-RELEASE-DATE::text").getall(),
        }

    def parse4(self, response):
        # from scrapy.shell import inspect_response
        custom_settings = {
            'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter'
        }

        # for i in range(len(response.css("L01-KEY::text"))):
        #     yield{
        #         "js id": response.css("L01-KEY::text")[i].get(),
        #         "arrest number": response.css("L01-ARREST-NO::text")[i].get(),
        #         "inmate name": response.css("L01-INMATE-NAME::text")[i].get(),
        #         "book date": response.css("L01-BOOK-DATE::text")[i].get(),
        #         "charge": response.css("L01-CHARGE::text")[i].get(),
        #     }

        # inspect_response(response, self)

        for i in range (len(response.css("L01-KEY::text"))):
            inmates_data = {
                "S101KEY": response.css("L01-KEY::text")[i].get(),
                "S101LIB": "DATACOLE",
                "S101PFX": "LE",
                "S101CNTY": "Coleman",
                "S101COCOD": "COLEM",
            }
            yield scrapy.FormRequest(url="https://netweb.netdatacorp.net/NDLEC/bok/CGIBOK101.ws", formdata=inmates_data, callback=self.parse3)
        
        