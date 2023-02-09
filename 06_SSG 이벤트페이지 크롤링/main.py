from bs4 import BeautifulSoup as bs
from typing import Dict,List
import requests as rq

class SSGEvent:
    def __init__(self) -> None:
        self.base_url : str = 'https://www.ssg.com/event/eventMain.ssg'
        self.headers : Dict[str,str] = {'User-Agent':'Mozilla/5.0'}
    
    @staticmethod
    def get_soup_obj(response:rq.Response)-> bs:
        return bs(response.text,'html.parser')
    
    def run(self)-> None:
        with rq.Session() as session:
            with session.get(url=self.base_url,headers=self.headers) as response:
                # Get soup Instance
                soup : bs = self.get_soup_obj(response=response)

                # Content Tag
                tag : str = 'div.content.active li.evt_osmu_unit'
                
                # Get Conent Length
                content_length : int = self.get_content_length(soup=soup,tag=tag)
                
                # Get Content
                results : List[Dict[str,str]] = self.get_content(soup=soup,content_length=content_length,tag=tag)

    def get_content_length(self,soup:bs,tag:str)-> int:
        return len(soup.select(tag))
    
    def get_content(self,soup:bs,content_length:int,tag:str)-> List[Dict[str,str]]:
        # Set Data List
        data_list : List[Dict[str,str]] = list()
        
        for idx in range(content_length):
            # Set Data Dict
            data_dict : Dict[str,str] = dict()
            
            # Get Content 
            contents : list = soup.select(tag)
            
            # Get title
            title = contents[idx].select_one('div.eo_tit > strong')
            if title == None:
                title = '-'
            else: 
                title = title.text.strip()
            
            # Get Description
            desc = contents[idx].select_one('p.desc1')
            if desc == None:
                desc = '-'
            else:
                desc = desc.text.strip()
            
            # Get Date
            date = contents[idx].select_one('span.eo_period > em')
            if date == None:
                date = '-'
            else:
                date = date.text.strip()
            
            # Get Brand
            brand = contents[idx].select_one('p.eo_mall > em')
            if brand == None:
                brand = '-'
            else:
                brand = brand.text.strip()
            
            # Get Link
            link = contents[idx].select_one('a.eo_link')
            if link == None:
                link = '-'
            else:
                link = link.attrs['href']
            
            # Save Data
            data_dict['title'] = title
            data_dict['desc'] = desc
            data_dict['date'] = date
            data_dict['brand'] = brand
            data_dict['link'] = link
            data_list.append(data_dict)
            
            # Print Data
            print(data_dict,'\n')
        
        # Return Datas
        return data_list
def main()-> None:
    # Create SSGEvent Instance
    ssg : SSGEvent = SSGEvent()
    
    # Run Method
    ssg.run()
    
if __name__ == '__main__':
    main()