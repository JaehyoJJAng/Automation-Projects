from __init__ import ViewTab
from typing import Dict,List
import requests as rq
import unittest

class ViewTabTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.view_tab : ViewTab = ViewTab()
    
    def test_get_soup_obj(self):
        base_url : str = self.view_tab.base_url
        
        with rq.Session() as session:
            with session.get(url=base_url,headers={'User-Agent':'Mozilla/5.0'}) as response:
                soup = self.view_tab.get_soup_obj(response=response)
                title : str = soup.select_one('a.api_txt_lines.total_tit').text.strip()                
                self.assertTrue(title)
    
    def test_run(self): 
        results : List[Dict[str,str]] = self.view_tab.run()
        self.assertEqual(len(results),8)
    
    def test_input_keyword(self):
        keyword : str = self.view_tab.keyword
        test_keyword = '블랙핑크'
        self.assertEqual(keyword,test_keyword)

if __name__ == '__main__':
    unittest.main()