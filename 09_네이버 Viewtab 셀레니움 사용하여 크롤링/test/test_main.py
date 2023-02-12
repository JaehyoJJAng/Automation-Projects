from __init__ import ViewTab
from typing import Dict,List
import requests as rq
import unittest

class ViewTabTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.view_tab : ViewTab = ViewTab()
    
    def test_get_soup_obj(self):
        # Get URL
        base_url : str = self.view_tab.url
        
        # Move Driver
        self.view_tab.browser.get(url=base_url)
        self.view_tab.browser.implicitly_wait(time_to_wait=10)        
        
        # Get soup object
        soup = self.view_tab.get_soup_obj(page_source=self.view_tab.browser.page_source)
        
        title_count : int = len(soup.select('a.total_tit'))
        self.assertEqual(title_count,7)
    
    def test_input_keyword(self):
        keyword : str = self.view_tab.keyword
        test_keyword = '블랙핑크'
        self.assertEqual(keyword,test_keyword)

    def test_scroll_down(self):
        self.view_tab.browser.get(url=f'https://search.naver.com/search.naver?where=view&sm=tab_jum&query={self.view_tab.keyword}')
        self.view_tab.browser.implicitly_wait(time_to_wait=10)
        self.view_tab.scroll_down()
        
        soup = self.view_tab.get_soup_obj(page_source=self.view_tab.browser.page_source)
        
        content_length : int = len(soup.select('div.timeline_cont._svp_item'))
        self.assertEqual(content_length,97)        
        
if __name__ == '__main__':
    unittest.main()