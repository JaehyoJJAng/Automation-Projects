from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs
from typing import List,Dict
import time
import re

class ChromeDriver:
    @staticmethod
    def setup_driver()-> webdriver.Chrome:
        # Creatge Options Instance
        options : Options = Options()
        
        # 크롬 창 자동으로 닫히지 않고 유지시키기
        options.add_experimental_option('detach',True)
        
        # Headless Mode
        options.add_argument('--headless')
        
        # Full Screen
        options.add_argument('--start-maximized')
        
        # 자동화 메시지 삭제
        options.add_experimental_option('excludeSwitches',['enable-automation'])
        
        # 불필요한 로깅 삭제
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        
        # User Agent 수정
        user_agent : str = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.3'
        options.add_argument(f'user-agent={user_agent}')
                
        # Create Service Instance
        service : Service = Service(ChromeDriverManager().install())
        
        # Create Driver Instance
        driver : webdriver.Chrome = webdriver.Chrome(service=service,options=options)
        
        # Driver return
        return driver

class MelonMobile:
    def __init__(self) -> None:                        
        # Set URL
        self.base_url : str = 'https://m2.melon.com/index.htm'
        
        # Get Driver Instance
        self.browser : webdriver.Chrome = ChromeDriver().setup_driver()

    def run(self)-> List[Dict[str,str]]:
        # Move Driver
        self.browser.get(url=self.base_url)
        self.browser.implicitly_wait(time_to_wait=10)
        
        # 이벤트 페이지 우회
        self.bypass_event_page()
        
        # 팝업 취소 클릭
        self.close_popup()
        
        # 멜론차트 클릭
        self.click_melon_chart()
        
        # 스크롤 한 번 내림
        self.scroll_down()
        
        # 더 보기 버튼 클릭
        self.more_btn()
        
        # 스크롤 한 번 내림
        self.scroll_down()

        # content loading wait
        time.sleep(2.0)

        # 컨텐츠 추출
        data_list : List[Dict[str,str]] = self.get_content()
        
        # 컨텐츠 리턴
        return data_list
    
    @staticmethod
    def get_soup_obj(page_source:str)-> bs:
        return bs(page_source,'html.parser')
    
    def get_content(self)-> List[Dict[str,str]]:
        # Content Tag
        content_tag : str = 'ul#_chartList li'
        
        # Get soup object
        soup : bs = self.get_soup_obj(page_source=self.browser.page_source)
        
        # Get Content Length
        content_length : int = len(soup.select('ul#_chartList li'))
        
        # Set Data List
        data_list : List[Dict[str,str]] = list()
        
        for idx in range(content_length):
            # Set Data Dict
            data_dict : Dict[str,str] = dict()
            
            # Get Contents
            contens : list = soup.select('ul#_chartList li')

            # thumbnail
            thumbnail = contens[idx].select_one('span.img')
            if thumbnail == None:
                continue
            else:
                thumbnail = re.sub('[\'\(\)]','',str(thumbnail.attrs['style']).split('background-image:url')[-1].replace('//',''))
            
            # title
            title = contens[idx].select_one('p.title')
            if title == None:
                title = '-'
            else:
                title = title.text.strip()
            
            # name
            name = contens[idx].select_one('span.name')
            if name == None:
                name = '-'
            else:
                name = name.text.strip()
            
            # Save Data
            data_dict['title'] = title
            data_dict['name']  = name
            data_dict['thumbnail'] = thumbnail
            data_list.append(data_dict)
            
            # Print Data
            print(data_dict,'\n')
            
        # return data_lisgt
        return data_list
    
    def more_btn(self)-> None:
        try:
            more_tag : str = 'button#moreBtn'
            
            self.browser.find_elements(By.CSS_SELECTOR,more_tag)[-2].click()
        except:
            print('pass')
    
    def scroll_down(self)-> None:
        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    
    def click_melon_chart(self)-> None:
        melon_chart_tag : str = 'ul.nav_wrap > li'
        self.browser.find_elements(By.CSS_SELECTOR,melon_chart_tag)[-3].click()
        time.sleep(1.0)
                
    def bypass_event_page(self)-> None:
        current_url : str = self.browser.current_url
        if current_url != self.base_url:
            self.browser.get(url=self.base_url)

    def close_popup(self)-> None:
        try :
            pop_close_tag : str = 'button.banner_full_close_today'
            self.browser.find_element(By.CSS_SELECTOR,pop_close_tag).click()
            time.sleep(1.0)
        except:
            pass        
    
def main()-> None:
    # Create Melon Instance
    melon : MelonMobile = MelonMobile()
    melon.run()

if __name__ == '__main__':
    main()        