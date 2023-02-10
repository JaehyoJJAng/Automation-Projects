from typing import Dict,List,Union
from bs4 import BeautifulSoup as bs
import requests as rq
import re

class MovieChart:
    def __init__(self) -> None:
        self._base_url : str = 'http://www.cgv.co.kr/movies/?lt=1&ft=0'
        self._headers  : Dict[str,str] = {'User-Agent':'Mozilla/5.0'}
    
    @staticmethod
    def get_soup_obj(response:rq.Response)-> bs:
        return bs(response.text,'html.parser')
    
    def run(self)-> None:
        with rq.Session() as session:
            with session.get(url=self._base_url,headers=self._headers) as response:
                soup : bs = self.get_soup_obj(response=response)
                
                # Movie Tag
                tag : str = 'div.wrap-movie-chart div.sect-movie-chart > ol > li'
                
                # Get movie length
                movie_length : int = self.get_movie_length(soup=soup,tag=tag)
                
                # Get Movie Content
                results : List[Dict[str,Union[str,int,float]]] = self.get_movie_content(soup=soup,movie_length=movie_length,tag=tag)

    def get_movie_length(self,soup:bs,tag:str)-> int:
        return len(soup.select(tag))
    
    def get_movie_content(self,soup:bs,movie_length:int,tag:str)-> List[Dict[str,Union[str,int,float]]]:
        # Set Data List
        data_list : List[Dict[str,Union[str,int,float]]] = list()
        
        for idx in range(movie_length):
            # Set Data Dict
            data_dict : Dict[str,Union[str,int,float]] = dict()
            
            # Get movie Content
            movie_content : list = soup.select(tag)
            
            # Get Title
            title = movie_content[idx].select_one('strong.title')
            if title == None:
                title = '-'
            else:
                title = title.text.strip()
                
            # Get Link
            link = movie_content[idx].select_one('div.box-contents > a')
            if link == None:
                link = '-'
            else:                
                link = link.attrs['href']                
                # startswith() 함수 사용하여 https 없는 경우에 대한 예외처리 진행
                if not link.startswith('https'):
                    link = 'http://www.cgv.co.kr/' + link
            
            # 예매율
            reservation_rate = movie_content[idx].select_one('div.score > strong > span')
            if reservation_rate == None:
                reservation_rate = 0.0
            else:
                reservation_rate = float(re.sub('[^0-9.]','',reservation_rate.text.strip()))
            
            # Egg Percent
            egg_percent = movie_content[idx].select_one('div.egg-gage.small > span.percent')
            if egg_percent == None:
                egg_percent = 0
            else:
                egg_percent = int(re.sub('[^0-9]','',egg_percent.text.strip()))
            
            # 개봉일자
            date = movie_content[idx].select_one('span.txt-info > strong')
            if date == None:
                date = '-'
            else:
                # next_element : 다음 요소를 가져옴 (<span>* 요소는 다른 엘리먼트이기에 안가져온 것)
                date = date.next_element.text.strip()
            
            # 썸네일
            thumbnail = movie_content[idx].select_one('span.thumb-image > img')
            if thumbnail == None:
                thumbnail = '-'
            else:
                thumbnail = thumbnail.attrs['src']
            
            # Save Data
            data_dict['title'] = title
            data_dict['reservation_rate'] = reservation_rate
            data_dict['egg_percent'] = egg_percent
            data_dict['date'] = date
            data_dict['thumbnail'] = thumbnail
            data_dict['link'] = link
            data_list.append(data_dict)
            
            # Print data
            print(data_dict,'\n')
        
        # Return data
        return data_list
def main():
    # Create MovieChart Instance
    movie : MovieChart = MovieChart()
    
    # Run method
    movie.run()

if __name__ == '__main__':
    main()