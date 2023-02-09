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
import time

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
        self.browser  : webdriver.Chrome = ChromeDriver().return_driver()
    
    @staticmethod
    def get_soup_obj(page_source:str)-> bs:
        return bs(page_source,'html.parser')
    
    def run(self)-> List[Dict[str,str]]:
        # View List
        view_data_list : List[Dict[str,str]] = list()
        
        # 브라우저 이동
        self.browser.get(url=self.base_url)
        self.browser.implicitly_wait(time_to_wait=15)
            
        # Scroll Down
        self.scroll_down(scroll_count=3)
                
        soup : bs = self.get_soup_obj(page_source=self.browser.page_source)
        
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
            
            # Print Data
            print(view_data_dict,'\n')
        # Return Data
        return view_data_list

    def scroll_down(self,scroll_count:int=3)-> None:
        # Clear Console
        os.system('clear')
        
        """ Browser Scroll Down """
        prev_height = self.browser.execute_script("return document.documentElement.scrollHeight")

        while scroll_count > 0:
            # 스크롤 내리기
            self.browser.execute_script("window.scrollTo(0 , document.documentElement.scrollHeight)")

            print(f'scrolling down ({scroll_count})')
            scroll_count -= 1

            # 대기시간 할당하기
            time.sleep(2)

            # 새로운 높이 값 받기
            curr_height = self.browser.execute_script("return document.documentElement.scrollHeight")

            # 이전 높이가 현재 높이와 같은경우 더보기 버튼 클릭
            if curr_height == prev_height:
                break

            prev_height = curr_height
    
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