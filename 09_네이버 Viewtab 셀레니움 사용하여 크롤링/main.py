from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict,List
from bs4 import BeautifulSoup as bs
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
        # Keyword
        self.keyword : str = self.input_keyword()
        
        # Set URL
        self.url : str = f'https://search.naver.com/search.naver?where=view&sm=tab_jum&query={rep.quote_plus(self.keyword)}'

        # Get Driver Instance
        self.browser : webdriver.Chrome = ChromeDriver().return_driver()
        
    def run(self)-> None:
        # Move Browser Page
        self.browser.get(url=self.url)
        self.browser.implicitly_wait(time_to_wait=15)
        
        # Scroll Down
        self.scroll_down()
        
        # Get soup object
        soup : bs = self.get_soup_obj(page_source=self.browser.page_source)
        
        # Get content
        data_lisgt : List[Dict[str,str]] = self.get_content(soup=soup)
        
    @staticmethod
    def get_soup_obj(page_source:str):
        return bs(page_source,'html.parser')
    
    def get_content(self,soup:bs)-> List[Dict[str,str]]:
        # Get Content Length
        content_length : int = len(soup.select('div.timeline_cont._svp_item'))
        
        # Set Data List
        data_list : List[Dict[str,str]] = list()
        
        for idx in range(content_length):
            # Set Data Dict
            data_dict : Dict[str,str] = dict()
            
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
            data_dict['title'] = title
            data_dict['link']  = link
            data_list.append(data_dict)

            # Print Data
            print(data_dict,'\n')
        # return data_list
        return data_list            
            
    def scroll_down(self)-> None:
        # Scroll pause time
        SCROLL_PAUSE_TIME : float = 1.0
        
        # Get scroll height
        last_height : int = self.browser.execute_script('return document.body.scrollHeight')
        
        # Scroll Count
        maximum_scroll : int = 5

        while True:
            if maximum_scroll == 0:
                break
            
            # Scroll down to bottom
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight-50);')
            time.sleep(SCROLL_PAUSE_TIME)
            
            # Calculate new scroll height and compare with last scroll height
            new_height : int = self.browser.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break
            
            last_height = new_height
            maximum_scroll -= 1
            
            # Print Scroll Count 
            print(maximum_scroll)

    def input_keyword(self)-> str:
        os.system('clear')
        while True:
            keyword : str = input('Input Keyword\n:')
            if not keyword:
                os.system('clear')
                print("No Keyword")
                continue
            return keyword            
        

def main():
    # Create ViewTab instance
    view_tab : ViewTab = ViewTab()    
    view_tab.run()

if __name__ == '__main__':
    main()