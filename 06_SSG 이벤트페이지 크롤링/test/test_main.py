from __init__ import SSGEvent
from typing import Dict,List
import requests as rq
import unittest

class SSGEventTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ssg : SSGEvent = SSGEvent()
    
    def test_get_soup_obj(self):
        with rq.Session() as session:
            with session.get(url=self.ssg.base_url,headers=self.ssg.headers) as response:
                # Get soup Instance
                soup  = self.ssg.get_soup_obj(response=response)                
                page_check : bool = False
                if '이벤트 & 쿠폰' in str(soup.text):
                    page_check = True                
                self.assertTrue(page_check)

    def test_get_content_length(self):
        with rq.Session() as session:
            with session.get(url=self.ssg.base_url,headers=self.ssg.headers) as response:
                # Get soup Instance
                soup  = self.ssg.get_soup_obj(response=response)
                
                # Content Tag
                tag : str = 'div.content.active li.evt_osmu_unit'
                
                # Get Conent Length
                content_length : int = self.ssg.get_content_length(soup=soup,tag=tag)
        self.assertEqual(content_length,97)
        
    def test_get_content(self):
        with rq.Session() as session:
            with session.get(url=self.ssg.base_url,headers=self.ssg.headers) as response:
                # Get soup Instance
                soup  = self.ssg.get_soup_obj(response=response)
                
                # Content Tag
                tag : str = 'div.content.active li.evt_osmu_unit'
                
                # Get Conent Length
                content_length : int = self.ssg.get_content_length(soup=soup,tag=tag)
        
                results: List[Dict[str,str]] = self.ssg.get_content(soup=soup,content_length=content_length,tag=tag)        
        self.assertEqual(len(results),97)
        
if __name__ == '__main__':
    unittest.main()