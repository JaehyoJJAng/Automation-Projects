from __init__ import create_dir , html_maker , get_env , Coupang
from pathlib import Path
from bs4 import BeautifulSoup as bs
from datetime import datetime
import unittest
import requests as rq
import os

class HtmlMakerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.coupang : Coupang = Coupang()
        
    def test_get_env(self):
        env_file : str = os.path.join(os.path.dirname(Path(__file__).resolve().parent),'ssh.env')
        
        env = get_env(env_file=env_file)
        
        host : str = env('host')
        user : str = env('user')
        self.assertTrue(host)
        self.assertTrue(user)
    
    def test_create_dir(self):
        file_path : str = 'testdir'
        create_dir(file_path=file_path)        
        
        dir_check : bool = os.path.isdir(file_path)
        self.assertTrue(dir_check)
        
    def tearDown(self):
        try :            
            os.rmdir('testdir')
        except:
            pass
    
    def test_html_maker(self):
        # File Path
        file_path : str = '/Users/jaehyolee/git/Inflearn-실습으로 끝장내는 파이썬 자동화 프로젝트/12_쿠팡 제품 크롤링 정보로 웹사이트 배포하기/html5up-massively'
                
        # File Name
        file_name : str = os.path.join(file_path,'index.html')
    
        # Create New Html
        html_maker(file_name=file_name,file_path=file_path,coupang=self.coupang)
        
        # title Check
        title_check : str = False
        
        # Date Check
        date_check  : str = datetime.now().strftime('%Y년 %m월 %d일')
        
        with open('html5up-massively/index.html','r') as html:            
            soup : bs = bs(html,'html.parser')
            
            title  = soup.select_one('header.major > h1').text.strip()
            if self.coupang.keyword in title:
                title_check = True
                
            date = soup.select_one('span.date').text.strip()
        
        self.assertEqual(date_check,date)
        self.assertTrue(title_check)
    
if __name__ == '__main__':
    unittest.main()