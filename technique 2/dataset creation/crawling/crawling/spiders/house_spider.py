import scrapy
import json

class PostsSpider(scrapy.Spider):
    name = "houses"

    jsonFile = open('links.json')

    data = json.load(jsonFile)
    
    start_urls =[]
    start_urls.append('https://www.hurriyetemlak.com/ankara-kecioren-senlik-satilik/daire/67085-874') #initial ad which has maximum features

    for element in data:
        if(element['link'] != None):
            start_urls.append('https://www.hurriyetemlak.com'+element['link'])

    def parse(self, response):

        featureNames = response.css('ul.adv-info-list span.txt::text').getall() 

        features = response.css('ul.adv-info-list span::text').getall()
        
        price = response.css('p.fontRB::text').get().strip()

        district = response.css('ul.short-info-list li::text').getall()[1].strip()

        neighborhood = response.css('ul.short-info-list li::text').getall()[2].strip()

        filteredFeatures = []


        for element in features:
            if(element == 'Cephe '):
                break  

            if not element in featureNames and element.find('/') == -1:
                filteredFeatures.append(element)
        
        featureNames = featureNames[0:len(filteredFeatures)] #to filter unused featureNames

        filteredFeatures.append(district)
        filteredFeatures.append(neighborhood)
        filteredFeatures.append(price)

        featureNames.append('Semt')
        featureNames.append('Mahalle')
        featureNames.append('Fiyat')


        # df2 = pd.DataFrame([filteredFeatures],columns=featureNames)
        
        houseData = dict(zip(featureNames, filteredFeatures))

        yield houseData
  
