import scrapy
from scrapy.selector import Selector
from pandas import Series, DataFrame
import re
import scrapy
import sys 

#scrapy runspider SpiderFincaRaiz.py -s LOG_ENABLED=False
class SpiderFincaRaiz(scrapy.Spider):
    name = "SpiderFincaRaiz"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0',
    }
    reload(sys)  
    sys.setdefaultencoding('latin-1')
    def start_requests(self):
        for s in range(20):
             
            url = "https://www.fincaraiz.com.co/casas/venta/bogota/?ad=30|%s||||1||9|||67|3630001|||400000000|||||||||||||1|||1||||||-1" % str(s)
            yield scrapy.Request(url=url, callback=self.parse)
            

    def parse(self, response):
        
        page = Selector(response).css('div .span-title a::attr(href)').extract()
    
        for href in page:
            yield scrapy.Request(response.urljoin(href),callback=self.parse_apartment)
            
    def getApartmentFeatures(self, response):
        featureResponse={}
      
        #featureResponse["fecha"] = [Selector(response).css('li:nth-child(1) .bold+ span::text').extract_first().replace("\r\n","")]
        featureResponse["precioTotal"] = [Selector(response).css('.price h2::text').extract_first().replace("\r\n","")]
        #featureResponse["title"] = [Selector(response).css('.detail_title span::text').extract_first().replace("\r\n","")]
        featureResponse["url"] = [response.url]
        features = {"precio metroCuadrado: " : u'Precio m\xb2:', "Area Privada: " : u'\xC1rea privada:', 'Estrato:': 'Estrato:',"Antiguedad: " : u'Antig\xfcedad:',"Admin: " : u'Adm\xf3n:'}
        for featureKey in features:
            if self.getFeatureValue (features[featureKey],response):
                featureResponse[featureKey]= [self.getFeatureValue (features[featureKey],response).replace("\r\n","").replace("m\xb2", "")]

        return featureResponse
         

    def getFeatureValue (self , feature, response):
        features = Selector(response).css('.features_2 b::text').extract()
        
        #print  "feature Values:", Selector(response).css('.features_2 li::text')[4].extract()
        for indexVal,featureName in enumerate (features):
            indexVal = indexVal + 1
            if  feature == featureName:
                if feature  == 'Estrato:':
                    return Selector(response).css('.features_2 li:nth-child(%s)::text'%str(indexVal))[1].extract()
                else:
                    return Selector(response).css('.features_2 li:nth-child(%s)::text'%str(indexVal))[0].extract()
    
    def parse_apartment(self, response):
       
        features = self.getApartmentFeatures(response)
        
        frame = DataFrame(features, columns=['sector', 'fecha','precioTotal', 'title','url','precio metroCuadrado: ','Area Privada: ','Estrato:','Antiguedad: ','Admin: '])
        
        
        with open(r'19.csv', 'a') as f:
                   frame.to_csv(f,encoding='latin-1',header=False, index=False)
        
          