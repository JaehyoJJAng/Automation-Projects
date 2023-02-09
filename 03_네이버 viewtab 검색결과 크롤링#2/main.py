from bs4 import BeautifulSoup as bs
from typing import List,Dict
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict,List,Union
from bs4 import BeautifulSoup as bs
import requests as rq
import os
import urllib.parse as rep

class ChromeDriver:
    @staticmethod
    def return_driver()-> webdriver.Chrome:
        # options 객체
        chrome_options : Options = Options()

        # headless Chrome 선언
        chrome_options.add_argument('--headless')

        # 브라우저 꺼짐 방지
        chrome_options.add_experimental_option('detach', True)

        # 불필요한 에러메시지 없애기
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        browser : webdriver.Chrome = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)    
        return browser

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
    
    def 
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
    
    # Run Method    
    view_tab.run()
    

if __name__ == '__main__':
    main()