from __init__ import DaumNews
from typing import Dict,List
import requests as rq
import unittest

class DaumNewsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.daum : DaumNews = DaumNews()
    
    def test_get_soup_obj(self):
        with rq.Session() as session:
            with session.get(url=self.daum.base_url,headers=self.daum.headers) as response:
                soup = self.daum.get_soup_obj(response=response)
                content_length : int = len(soup.select('div.item_issue'))
        self.assertEqual(content_length,20)
    
    def test_get_content_length(self):
        with rq.Session() as session:
            with session.get(url=self.daum.base_url,headers=self.daum.headers) as response:
                soup = self.daum.get_soup_obj(response=response)
                content_length : int = self.daum.get_content_length(soup=soup,tag='div.item_issue')
        self.assertEqual(content_length,20)
    
    def test_get_news_content(self):    
        with rq.Session() as session:
            with session.get(url=self.daum.base_url,headers=self.daum.headers) as response:
                soup = self.daum.get_soup_obj(response=response)
                content_length : int = self.daum.get_content_length(soup=soup,tag='div.item_issue')
                
                results : List[Dict[str,str]] = self.daum.get_news_content(soup=soup,content_length=content_length,tag='div.item_issue')
        self.assertEqual(len(results),20)

if __name__ == '__main__':
    unittest.main()    