from config.config import get_headers
from bs4 import BeautifulSoup as bs
from typing import Dict,List
import requests as rq
import os
import urllib.parse as rep

class Coupang:
    def __init__(self) -> None:
        # Headers
        self._headers : Dict[str,str] = get_headers()
        
        # Set Keyword
        self.keyword : str = self.input_keyword()
        
        # Set Page Count
        self.page_count : int = self.input_page()
        
        
    @staticmethod
    def get_soup_obj(response:rq.Response)-> bs:
        return bs(response.text,'html.parser')
    
    def run(self):
        # Set URLS
        urls : List[str] = [f'https://www.coupang.com/np/search?q={rep.quote_plus(self.keyword)}&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=rocket,rocket_wow,coupang_global&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={self.page_count}&rocketAll=true&searchIndexingToken=1=6&backgroundColor=' for page in range(1,self.page_count + 1)]
        
        # Session
        with rq.Session() as session:
            [self.fetch(session,url=url) for url in urls]

    def fetch(self,session:rq.Session,url:str):
        with session.get(url=url,headers=self._headers) as response:
            # Get Soup Object
            soup : bs = self.get_soup_obj(response=response)
            
            # Prod Tag
            tag : str = 'ul#productList > li'
            
            # Get Prod Length
            content_length : int = self.get_prod_length(soup=soup,tag=tag)
            print(content_length)
    
    def get_prod_length(self,soup:bs,tag:str)-> int:
        return len(soup.select(tag))
    
    def get_prod(self):
        pass
        
    def input_page(self)-> int:
        os.system('clear')
        while True:
            page_count : str = input('Input Page Count\n:')
            if not page_count:
                os.system('clear')
                print("No page count")
                continue
            return int(page_count)
        
    def input_keyword(self)-> str:
        # Clear Console Log
        os.system('clear')        
        while True:
            keyword : str = input('Input Keyword\n\n:')
            if not keyword:
                os.system('clear')
                print("No Keyword")
                continue
            return keyword        
    
def main():
    # Create Couapng Instance
    coupang : Coupang = Coupang()
    
    # Run Method
    coupang.run()

if __name__ == '__main__':
    main()