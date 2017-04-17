import scrapy
from scrapy.selector import Selector
from pandas import Series, DataFrame


import scrapy


class SpiderFincaRaiz(scrapy.Spider):
    name = "SpiderFincaRaiz"
    #scrapy shell "https://www.fincaraiz.com.co/apartamentos/venta/bogota/?ad=30|1||||1||8|||67|3630001|||300000000|||||||||||||1|||1||||||-1"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0',
    }
    def start_requests(self):
        for s in range(2):
    
          url="https://www.fincaraiz.com.co/apartamentos/venta/bogota/?ad=30|%s||||1||8|||67|3630001|||300000000|||||||||||||1|||1||||||-1" %str(s)
          yield scrapy.Request(url=url, callback=self.parse)
            

    def parse(self, response):
        
        page = Selector(response).css('div .span-title a::attr(href)').extract()
        print "saul"

        for href in page:
            yield scrapy.Request(response.urljoin(href),callback=self.parse_apartment)
        
    def parse_apartment(self, response):
        
        if Selector(response).css('dt.property.bold.dt::text')[3].extract() == 'Estrato:':
            print 'sas'

       
        # table = [[1 , 2], [3, 4]]
        # onclick=announcements.css('al[class="advert  Product_Code_DON AD_OV"]::attr(onclick)').extract()

        
        # print "place" ,len(onclick)
        # frame = DataFrame({'title':onclick},columns=['onclick'])
        
       
        
        
        # with open(r'out14.csv', 'a') as f:
        #            frame.to_csv(f, encoding='utf-8',header=False)
      