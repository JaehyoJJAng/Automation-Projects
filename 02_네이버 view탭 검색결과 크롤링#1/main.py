from bs4 import BeautifulSoup as bs
from typing import List,Dict
import requests as rq
import os
import urllib.parse as rep

class ViewTab:
    def __init__(self) -> None:
        self.keyword  : str = self.input_keyword()
        self.base_url : str = f'https://search.naver.com/search.naver?where=view&sm=tab_jum&query={rep.quote_plus(self.keyword)}'
    
    @staticmethod
    def get_soup_obj(response:rq.Response)-> bs:
        return bs(response.text,'html.parser')
    
    def run(self)-> List[Dict[str,str]]:
        # View List
        view_data_list : List[Dict[str,str]] = list()
        
        # Open Session
        with rq.Session() as session:
            with session.get(url=self.base_url,headers={'User-Agent':'Mozilla/5.0'}) as response:
                soup : bs = self.get_soup_obj(response=response)
                
                # Content Length
                content_length : int = len(soup.select('div.timeline_cont._svp_item'))
                
                for idx in range(content_length):
                    # View Dict
                    view_data_dict : Dict[str,str] = dict()
                    
                    # Get Contents
                    contents : list = soup.select('div.timeline_cont._svp_item')
                    
                    # Get Title & Get Link
                    title : str = contents[idx].select_one('a.api_txt_lines.total_tit')
                    if title == None or title.text == '':
                        title = '-'
                        link = '-'
                    else:
                        link : str = title.attrs['href']
                        title = title.text.strip()
                    
                    # Save Data
                    view_data_dict['title'] = title
                    view_data_dict['link']  = link
                    view_data_list.append(view_data_dict)
        # Return Data
        return view_data_list
    
    def input_keyword(self)-> str:
        os.system('clear')
        while True:
            keyword : str = input('키워드\n:')
            if not keyword:
                os.system('clear')
                print('No Keyword')
                continue                
            return keyword

def main()-> None:
    # ViewTab Instance
    view_tab : ViewTab = ViewTab()
    
    view_tab.run()

if __name__ == '__main__':
    main()