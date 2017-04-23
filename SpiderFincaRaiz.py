import scrapy
from scrapy.selector import Selector
from pandas import Series, DataFrame
import re

import scrapy


class SpiderFincaRaiz(scrapy.Spider):
    name = "SpiderFincaRaiz"
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0',
    }
    def start_requests(self):
        for s in range(2):
    
          url="https://www.fincaraiz.com.co/apartamentos/venta/bogota/?ad=30|%s||||1||8|||67|3630001|||300000000|||||||||||||1|||1||||||-1" %str(s)
          yield scrapy.Request(url=url, callback=self.parse)
            

    def parse(self, response):
        
        page = Selector(response).css('div .span-title a::attr(href)').extract()
        

        for href in page:
            yield scrapy.Request(response.urljoin(href),callback=self.parse_apartment)
        
    def parse_apartment(self, response):
        #run > scrapy runSpider SpiderFincaRaiz
        line = Selector(response).css('dt.property.bold.dt::text')[1].extract()
        line2 = Selector(response).css('dt.property.bold.dt::text')[2].extract()
        print "*****************************************" 
        print response.url
        print "Precio Total: " ,Selector(response).css('span.display.bold::text')[0].extract()
        # display bold 
        if Selector(response).css('dt.property.bold.dt::text')[3].extract() == 'Estrato:':
            print "Estrato: "+Selector(response).css('dd.dd::text')[3].extract()
        if  Selector(response).css('dt.property.bold.dt::text')[0].extract() == u'\xC1rea Const.:':
            print "Area construida "+ Selector(response).css('dd.dd::text')[0].extract()
        if  Selector(response).css('dt.property.bold.dt::text')[1].extract() == u'\xC1rea privada:':
            print"Area privada "+ Selector(response).css('dd.dd::text')[1].extract()
        if  'Precio metro cuadrado' in line :
            print "Precio : " , Selector(response).css('dd.dd::text')[1].extract()  
        if  'Precio' in line2:
            print "Precio metro cuadrado: " + Selector(response).css('dd.dd::text')[2].extract()   
        print "*****************************************"  