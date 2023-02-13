from config.config import get_headers
from bs4 import BeautifulSoup as bs
from typing import Dict,List,Union
import requests as rq
import os
import urllib.parse as rep
import time

class Coupang:
    def __init__(self) -> None:
        # Headers
        self._headers : Dict[str,str] = get_headers()
        
        # Set Keyword
        self.keyword : str = self.input_keyword()
        
        # Set Page Count
        self.page_count : int = self.input_page()
        
        # Set Prod Count
        self.prod_count : int = 1
        
    @staticmethod
    def get_soup_obj(response:rq.Response)-> bs:
        return bs(response.text,'html.parser')
    
    def run(self)-> List[List[Dict[str,Union[str,int,float]]]]:
        # Set URLS
        urls : List[str] = [f'https://www.coupang.com/np/search?q={rep.quote_plus(self.keyword)}&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=rocket,rocket_wow,coupang_global&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={self.page_count}&rocketAll=true&searchIndexingToken=1=6&backgroundColor=' for page in range(1,self.page_count + 1)]
        
        # Session
        with rq.Session() as session:
            return [self.fetch(session,url=url) for url in urls]

    def fetch(self,session:rq.Session,url:str)-> List[Dict[str,Union[str,int,float]]]:
        with session.get(url=url,headers=self._headers) as response:
            # Get Soup Object
            soup : bs = self.get_soup_obj(response=response)
            
            # Prod Tag
            tag : str = 'ul#productList > li'
            
            # Get Prod Length
            prod_length : int = self.get_prod_length(soup=soup,tag=tag)
            
            # Get Prod Content
            data_list : List[Dict[str,Union[str,int,float]]] = self.get_prod(soup=soup,prod_length=prod_length,tag=tag)
        
        # return data_list
        return data_list
    
    def get_prod_length(self,soup:bs,tag:str)-> int:
        return len(soup.select(tag))
    
    def get_prod(self,soup:bs,prod_length:int,tag:str)-> List[Dict[str,Union[str,int,float]]]:
        # Set Data List
        data_list : List[Dict[str,Union[str,int,float]]] = list()
        
        for idx in range(prod_length):
            # Set Data Dict
            data_dict : Dict[str,Union[str,int,float]] = dict()
            
            # Get Products
            prods : list = soup.select(tag)
            
            # Ad Check
            ad = prods[idx].select_one('span.ad-badge-text')
            if ad:
                continue
            
            # Get Thumbnail
            thumbnail = prods[idx].select_one('img.search-product-wrap-img')
            if thumbnail == None:
                continue
            else:
                # attrs : 해당 키가 없으면 에러
                # get : 해당 키가 없으면 None return
                if thumbnail.get('data-img-src') == None:
                    thumbnail = 'https:' + thumbnail.attrs['src']
                else:
                    thumbnail = 'https:' + thumbnail.get('data-img-src')
                    
                # 이미지 크기 커스텀
                thumbnail = thumbnail.replace('230x230ex','1000x1000ex')
            
            # Get Title
            title = prods[idx].select_one('div.name')
            if title == None:
                title = '-'
            else:
                title = title.text.strip()
            
            # Get Prod Link
            link = prods[idx].select_one('a.search-product-link')
            if link == None:
                link = '-'
            else: 
                link = 'https://www.coupang.com' + link.attrs['href']
            
            # Get Price
            price = prods[idx].select_one('strong.price-value')
            if price == None:
                price = 0
            else:
                # isdigt() 함수 활용하여 ',' 제거 (숫자만 추출))
                price = ''.join([num for num in price.text.strip() if num.isdigit()])
            
            # Get rating
            rating = prods[idx].select_one('em.rating')
            if rating == None:
                rating = 0.0
            else:
                rating = float(rating.text.strip())
                        
            # Get Reviews 
            reviews = prods[idx].select_one('span.rating-total-count')
            if reviews == None:
                reviews = 0
            else:
                # isdigit() 함수 활용하여 '()' 제거 (숫자만 추출)
                reviews = ''.join([num for num in reviews.text.strip() if num.isdigit()])
            
            # Save Data
            data_dict['prod_count'] = self.prod_count
            data_dict['title'] = title
            data_dict['price'] = price
            data_dict['rating'] = rating
            data_dict['reviews'] = reviews
            data_dict['link'] = link
            data_dict['thumbnail'] = thumbnail
            data_list.append(data_dict)
            
            # Print Data
            print(f'{data_dict}\n')
            
            # Prod Count Add
            self.prod_count += 1
        
        # Return data
        return data_list
    
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