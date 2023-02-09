from __init__ import MelonTop100
from typing import Dict,List
import requests as rq
import unittest

class MelonTop100Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.melon : MelonTop100 = MelonTop100()
    
    def test_get_soup_obj(self):
        with rq.Session() as session:
            with session.get(url=self.melon.base_url,headers={'User-Agent':'Mozilla/5.0'}) as response:
                soup = self.melon.get_soup_obj(response=response)
                content_length : int = len(soup.find_all(class_=['lst50','lst100']))
        self.assertEqual(content_length,100)        
    
    def test_fetch(self):
        with rq.Session() as session:
            results : List[Dict[str,str]] = self.melon.fetch(session=session)
        self.assertEqual(len(results),100)
    
    def test_get_id(self):
        num : int = self.melon.get_id(song_num_text='금년 온도지수 233243201')
        self.assertEqual(num,233243201)

if __name__ == '__main__':
    unittest.main()