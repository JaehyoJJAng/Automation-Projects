from typing import Dict,List
from bs4 import BeautifulSoup as bs
import requests as rq

class DaumNews:
    def __init__(self) -> None:
        self.base_url : str = 'https://news.daum.net/'
        self.headers : Dict[str,str] = {'User-Agent':'Mozilla/5.0'}
    
    @staticmethod
    def get_soup_obj(response:rq.Response)-> bs:
        return bs(response.text,'html.parser')
    
    def run(self)-> None:
        with rq.Session() as session:
            with session.get(url=self.base_url,headers=self.headers) as response:
                soup : bs = self.get_soup_obj(response=response)
                
                # Get Content Length
                content_length : int = self.get_content_length(soup=soup,tag='div.item_issue')
                
                # Get News Content Data
                news_data : List[Dict[str,str]] = self.get_news_content(soup,content_length=content_length,tag='div.item_issue')

    def get_content_length(self,soup:bs,tag:str)-> int:
        return len(soup.select(tag))
    
    def get_news_content(self,soup:bs,content_length:int,tag:str)-> List[Dict[str,str]]:
        # Set News Data List
        news_data_list : List[Dict[str,str]] = list()
        
        for idx in range(content_length):
            # Set News Data Dict
            news_data_dict : Dict[str,str] = dict()
            
            # Get Content
            contents : list = soup.select(tag)
            
            # Get title & Get Link
            title = contents[idx].select_one('a.link_txt')
            link : str = '-'
            if title == None:
                title = '-'
            else:
                link = title.attrs['href']
                title = title.text.strip()
                
            # Get Platform
            platform : str = contents[idx].select_one('div.cont_thumb span.logo_cp > img')
            if platform == None:
                platform = '-'
            else:
                platform = platform.attrs['alt']

            # Get Category
            category : str = contents[idx].select_one('span.txt_category')
            if category == None:
                category = '-'
            else:
                category = category.text.strip()
            
            # Get Thumbnail
            thumbnail : str = contents[idx].select('img.thumb_g')
            if len(thumbnail) == 0:
                thumbnail = '-'
            else:
                thumbnail = thumbnail[0].attrs['src']
            
            # Save Data
            news_data_dict['title'] = title
            news_data_dict['platform'] = platform
            news_data_dict['category'] = category
            news_data_dict['thumbnail'] = thumbnail
            news_data_dict['link'] = link
            news_data_list.append(news_data_dict)

            # Print Data
            print(news_data_dict,'\n')
        # Return Data
        return news_data_list
    
def main()-> None:
    # Create DaumNews Instance
    daum : DaumNews = DaumNews()
    
    # Run Method
    daum.run()

if __name__ == '__main__':
    main()