import scrapy


class BoyzSpider(scrapy.Spider):
    name = "boyzadams"
    start_urls = ["http://www.adamscosheriff.org/inmate-roster"]

    def parse(self, response):
        # from scrapy.shell import inspect_response
        # from scrapy.utils.response import open_in_browser

        # open_in_browser(response)
        # inspect_response(response, self)

        boyz = response.css("div.sidebar-inmate-list-item")
        for element in response.css("p.profile-link a::attr(href)"):
            for boy in boyz:
                view_profile = element.get()
                if view_profile is not None:
                    yield response.follow(view_profile, callback=self.parseInmate)

        
        next_page = response.css("a.next.page-numbers::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
            
 
    def parseInmate(self, response):
        for data in response.css("div.inmate-info"):
            yield{
                "full name": data.css("p::text")[0].get(),               
                "booking number": data.css("p::text")[1].get().replace(" ",""), 
                "age": data.css("p::text")[2].get().replace(" ",""), 
                "gender": data.css("p::text")[3].get().replace(" ",""), 
                "race": data.css("p::text")[4].get().replace(" ",""), 
                "address": data.css("p::text")[5].get().replace(" ",""), 
                "booking date": data.css("p::text")[7].get().replace(" ",""), 
                "charges": data.css("p::text")[8].get(), 
                "bond": data.css("p::text")[9].get().replace(" ",""), 
            }