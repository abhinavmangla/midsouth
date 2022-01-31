#Created by: Abhinav Mangla 
#01 Feb 2022

from shutil import which
import scrapy
from bs4 import BeautifulSoup
import json

class ExtractUrls(scrapy.Spider):
    name = "extract"
  
    def start_requests(self):
        urls = [ 'https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage=1', ]
          
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)
  
    
    def parse(self, response):
        result_list = []
        data = BeautifulSoup(response.body, 'lxml')
        all_products = data.find_all('div', {'class':'product'})
        for i in range(len(all_products)):
            temp = all_products[i].find_all('a', {'class':'catalog-item-name'})
            title = temp[0].text
            temp = all_products[i].find_all('span', {'class':'price'})
            price = float(temp[0].text[1:])
            temp = all_products[i].find_all('span', {'class':'status'})
            if temp[0].text=='Out of Stock':
                status = False
            else:
                status = True
            temp = all_products[i].find_all('a', {'class':'catalog-item-brand'})
            maftr = temp[0].text
            append_dict = {'price':price, 'title':title, 'stock':status, 'maftr':maftr}
            result_list.append(append_dict)
        json_obj = json.dumps(result_list)
        with open('result.json', 'w') as outfile:
            outfile.write(json_obj)
        print('Written to JSON')

            



          
        # # Extra feature to get title
        # title = response.css('title::text').extract_first() 
          
        # # Get anchor tags
        # links = response.css('a::attr(href)').extract()     
          
        # for link in links:
        #     yield 
        #     {
        #         'title': title,
        #         'links': link
        #     }
              
        #     if 'geeksforgeeks' in link:         
        #         yield scrapy.Request(url = link, callback = self.parse)