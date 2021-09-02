import scrapy

class PostsSpider(scrapy.Spider):
    name = "links"

    start_urls = [
        'https://www.hurriyetemlak.com/ankara-satilik?page=1',
    ]

    def parse(self, response):
              
        baseLink = 'https://www.hurriyetemlak.com/ankara-satilik?page='
        numberOfPages = 100 # response.css('li.page-item a::text').getall()[6]
        currentPageNumber = 1

        for post in response.css('div.links'):
            yield{
                'link': post.css('a.card-link::attr(href)').get()
            }
            
        while currentPageNumber != numberOfPages:
            currentPageNumber +=1
            nextPage = baseLink+str(currentPageNumber)
            yield scrapy.Request(nextPage, callback=self.parse)
