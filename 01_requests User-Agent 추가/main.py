from bs4 import BeautifulSoup as bs
from typing import Dict
import requests as rq

def get_response(url:str,headers:Dict[str,str])-> rq.Response:
    return rq.get(url=url,headers=headers)

def main():      
    # Headers 선언
    headers : Dict[str,str] = {'User-Agent' : 'Mozilla/5.0'}

    # Set URL
    url : str = 'https://www.naver.com'  
    
    # Get response
    req : rq.Response = get_response(url=url,headers=headers)
    
    # req dir print
    # print(dir(req))
    
    # req.reques.header
    print(req.request.headers)
    
    # 디폴트 User-Agent는 아래와 같으므로 차단 가능성이 높아짐
    """ 
    {'User-Agent': 'python-requests/2.28.2', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
    """
    
if __name__ == '__main__':
    main()