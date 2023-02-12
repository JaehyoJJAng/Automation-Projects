from __init__ import MelonMobile
from typing import Dict,List
from selenium.webdriver.common.by import By
import requests as rq
import unittest
import time

class MelonMobileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.melon : MelonMobile = MelonMobile()
    
    def test_get_soup_obj(self):
        base_url : str = 'https://www.naver.com/'
        text : str = '네이버'
        self.melon.browser.get(url=base_url)
        self.melon.browser.implicitly_wait(time_to_wait=10)
        
        page_check : bool = False
        if text in self.melon.browser.page_source:
            page_check = True
        self.assertTrue(page_check)
    
    def test_get_content(self):
        self.melon.browser.get(url=self.melon.base_url)
        self.melon.browser.implicitly_wait(time_to_wait=10)        
        
        # Bypass
        self.melon.bypass_event_page()

        # Close pop up
        self.melon.close_popup()
        
        # Click Melon Chart
        self.melon.click_melon_chart()
        
        # Click More Button
        self.melon.more_btn()
        
        # Time Wait
        time.sleep(2.0)
        
        # Data List
        data_list : List[Dict[str,str]] = self.melon.get_content()
        self.assertEqual(len(data_list),100)
    
    def test_more_btn(self):
        self.melon.browser.get(url=self.melon.base_url)
        self.melon.browser.implicitly_wait(time_to_wait=10)        
        
        # Bypass
        self.melon.bypass_event_page()

        # Close pop up
        self.melon.close_popup()
        
        # Click More Button
        self.melon.more_btn()
    
        # Time Wait
        time.sleep(2.0)
        
        length : int = len(self.melon.browser.find_elements(By.CSS_SELECTOR,'ul#_chartList li'))
        self.assertEqual(length,100)
    
    def test_scroll_down(self):
        self.melon.browser.get(url=self.melon.base_url)
        self.melon.browser.implicitly_wait(time_to_wait=10)        
        self.melon.scroll_down()        
    
    def test_click_melon_chart(self):
        self.melon.browser.get(url=self.melon.base_url)
        self.melon.browser.implicitly_wait(time_to_wait=10)        
        
        # Bypass
        self.melon.bypass_event_page()

        # Close pop up
        self.melon.close_popup()
        
        # Click Melon Chart
        self.melon.click_melon_chart()
    
    def test_bypass_event_page(self):
        tag : str = 'div#naviMenu li'
        self.melon.browser.get(url=self.melon.base_url)
        self.melon.browser.implicitly_wait(time_to_wait=10)        
        self.melon.bypass_event_page()
        length : int = len(self.melon.browser.find_elements(By.CSS_SELECTOR,tag))
        self.assertEqual(length,5)
    
    def test_close_popup(self):
        self.melon.browser.get(url=self.melon.base_url)
        self.melon.browser.implicitly_wait(time_to_wait=10)        
        
        # Bypass
        self.melon.bypass_event_page()

        # Close pop up
        self.melon.close_popup()
        
if __name__ == '__main__':
    unittest.main()