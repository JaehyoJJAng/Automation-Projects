from typing import Dict,List
from bs4 import BeautifulSoup as bs
import requests as rq

class DaumNews:
    def __init__(self) -> None:
        self.base_url : str = 'https://news.daum.net/'
        self.headers : Dict[str,str] = {'User-Agent':'Mozilla/5.0'}
    
    @staticmethod
    def get_soup_obj(response:rq.Response)-> bs:
        return bs(response.text,'html.parser')
    
    def run(self)-> None:
        with rq.Session() as session:
            with session.get(url=self.base_url,headers=self.headers) as response:
                soup : bs = self.get_soup_obj(response=response)
                
                # Get Content Length
                content_length : int = self.get_content_length(soup=soup,tag='div.item_issue')                
                    
    def get_content_length(self,soup:bs,tag:str)-> int:
        return len(soup.select(tag))
    
    def get_news_content(self)-> None:
        pass

def main()-> None:
    # Create DaumNews Instance
    daum : DaumNews = DaumNews()
    
    # Run Method
    daum.run()

if __name__ == '__main__':
    main()