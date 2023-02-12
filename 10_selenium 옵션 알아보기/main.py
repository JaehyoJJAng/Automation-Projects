from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pathlib import Path

class ChromeDriver:
    @staticmethod
    def setup_driver():
        # Creatge Options Instance
        options : Options = Options()
        
        # 크롬 창 자동으로 닫히지 않고 유지시키기
        options.add_experimental_option('detach',True)
        
        # Headless Mode
        options.add_argument('--headless')
        
        # Full Screen
        options.add_argument('--start-maximized')
        
        # Mute
        options.add_argument('--mute-audio')
        
        # Secret Mode
        options.add_argument('incognito')
        
        # 자동화 메시지 삭제
        options.add_experimental_option('excludeSwitches',['enable-automation'])
        
        # 불필요한 로깅 삭제
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        
        # User Agent 수정
        user_agent : str = 'ozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Whale/3.19.166.16 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        
        # 유저 데이터 추가
        user_data : str = Path(__file__).resolve().parent + '/user-data-dir'
        options.add_argument(f'user-data-dir={user_data}')
                
        # Create Service Instance
        service : Service = Service(ChromeDriverManager().install)
        
        # Create Driver Instance
        driver : webdriver.Chrome = webdriver.Chrome(service=service,options=options)
        
        
