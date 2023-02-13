from __init__ import Coupang
from typing import Dict,List,Union
import requests as rq
import urllib.parse as rep
import unittest
import os

class CoupangTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.coupang : Coupang = Coupang()
        cls.url : str = f'https://www.coupang.com/np/search?q={rep.quote_plus(cls.coupang.keyword)}&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=rocket,rocket_wow,coupang_global&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={cls.coupang.page_count}&rocketAll=true&searchIndexingToken=1=6&backgroundColor='
        
    def test_get_soup_obj(self):
        with rq.Session() as session:
            with session.get(url=self.url,headers=self.coupang._headers) as response:
                soup = self.coupang.get_soup_obj(response=response)                
                page_check : bool = False
                if self.coupang.keyword in str(soup.text):
                    page_check = True
                self.assertTrue(page_check)

    def test_fetch(self):
        with rq.Session() as session:            
            results : List[Dict[str,Union[str,int,float]]] = self.coupang.fetch(session=session,url=self.url)
        self.assertGreater(a=len(results),b=28)
        
    def test_get_prod_length(self):
        with rq.Session() as session:
            with session.get(url=self.url,headers=self.coupang._headers) as response:
                soup = self.coupang.get_soup_obj(response=response)
                tag : str = 'ul#productList > li'
                prod_length : int = self.coupang.get_prod_length(soup=soup,tag=tag)
        self.assertGreater(a=prod_length,b=28)
        
    
    def test_get_prod(self):
        with rq.Session() as session:
            with session.get(url=self.url,headers=self.coupang._headers) as response:
                soup = self.coupang.get_soup_obj(response=response)
                tag : str = 'ul#productList > li'
                prod_length : int = self.coupang.get_prod_length(soup=soup,tag=tag)
                
                results : List[Dict[str,Union[str,int,float]]] = self.coupang.get_prod(soup=soup,prod_length=prod_length,tag=tag)        
        self.assertGreater(a=len(results),b=28)
        
    def test_input_keyword(self):
        test_keyword : str = '마우스'
        self.assertEqual(self.coupang.keyword,test_keyword)
    
    def test_input_page(self):
        test_page : int = 1
        self.assertEqual(self.coupang.page_count,test_page)

if __name__ == '__main__':
    unittest.main()