from bs4 import BeautifulSoup as bs
from typing import Dict,List
import requests as rq


class SSGEvent:
    def __init__(self) -> None:
        self.base_url : str = 'https://www.ssg.com/event/eventMain.ssg'
        self.headers : Dict[str,str] = {'User-Agent':'Mozilla/5.0'}
    
    @staticmethod
    def get_soup_obj(response:rq.Response):
        return bs(response.text,'html.parser')
    
    def run(self):
        with rq.Session() as session:
            with session.get(url=self.base_url,headers=self.headers) as response:
                # Get soup Instance
                soup : bs = self.get_soup_obj(response=response)

                # Content Tag
                tag : str = 'div.content.active li.evt_osmu_unit'
                
                # Get Content Length
                content_length : int = self.get_content_length(soup=soup,tag=tag)
                            
    def get_content_length(self,soup:bs,tag:str)-> int:
        return len(soup.select(tag))
    
    def get_content(self):
        pass

def main():
    # Create SSGEvent Instance
    ssg : SSGEvent = SSGEvent()
    
    # Run Method
    ssg.run()
    
if __name__ == '__main__':
    main()