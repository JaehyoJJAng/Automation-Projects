from bs4 import BeautifulSoup as bs 
from typing import Dict,List,Union
import requests as rq
import re

class MelonTop100:
    def __init__(self) -> None:
        self.base_url : str = 'https://www.melon.com/chart/index.htm'
    
    def run(self)-> None:
        with rq.Session() as session:
            results : List[Dict[str,str]] = self.fetch(session=session)

    @staticmethod
    def get_soup_obj(response:rq.Response)-> bs:
        return bs(response.text,'html.parser')
    
    def fetch(self,session:rq.Session)-> List[Dict[str,str]]:
        # Set Album Data List
        album_data_list : List[Dict[str,str]] = list()
        
        # Open Session
        with session.get(url=self.base_url,headers={'User-Agent':'Mozilla/5.0'}) as response:
            if response.ok:                
                soup : bs = self.get_soup_obj(response=response)
                
                # Get Content Length
                content_length : int = len(soup.find_all(class_=['lst50','lst100']))
                
                # Song Count
                count : int = 1
                
                # For Loop
                for idx in range(content_length):
                    # Set Album Data Dict
                    album_data_dict : Dict[str,str] = dict()
                    
                    # Get Contents
                    contents : list = soup.find_all(class_=['lst50','lst100'])
                    
                    # Get Song Title
                    title = contents[idx].select_one('div.ellipsis.rank01')
                    if title == None:
                        continue
                    else:
                        
                        title = title.text.strip()
                    
                    # Get Artist & Get Artist channel ID
                    artist = contents[idx].select_one('div.ellipsis.rank02')
                    artist_channel_id : Union[int,None] = None                    
                    if artist == None:
                        artist = '-'
                    else:
                        artist_channel_id = self.get_id(song_num_text=artist.select_one('a').attrs['href'])
                        artist = artist.text.strip()
                    
                    # Get Album & Get Album ID
                    album = contents[idx].select_one('div.ellipsis.rank03')
                    album_id : Union[int,None] = 0
                    if album == None:
                        album = '-'
                    else:
                        album_id = self.get_id(song_num_text=album.select_one('a').attrs['href'])
                        album = album.text.strip()
                    
                    # Get Thumbnail
                    thumbnail = contents[idx].select_one('a.image_typeAll > img')
                    if thumbnail == None:
                        thumbnail = '-'
                    else:
                        thumbnail = thumbnail.attrs['src']
                    
                    # Set Album Link
                    album_link : str = '-'
                    if album_id == None:
                        pass
                    else:
                        album_link = f'https://www.melon.com/album/detail.htm?albumId={album_id}'
                    
                    # Set Artist Channel Link
                    artist_channel_link : str = '-'
                    if artist_channel_id == None:
                        pass
                    else:
                        artist_channel_link = f'https://www.melon.com/artist/timeline.htm?artistId={artist_channel_id}'
                    
                    # Save Data
                    album_data_dict['title']  = title
                    album_data_dict['artist'] = artist
                    album_data_dict['album']  = album
                    album_data_dict['thumbnail'] = thumbnail
                    album_data_dict['artist_channel_link'] = artist_channel_link
                    album_data_dict['album_link'] = album_link           
                    album_data_list.append(album_data_dict)
                    
                    # Print Data
                    print(f'{album_data_dict}\n')                    
                    
                    # Up Count
                    count += 1
        # Return Data
        return album_data_list

    def get_id(self,song_num_text:str)-> int:
        song_num : List[int] = list()
        for num in song_num_text:
            # text.isdigit() = True or False
            if num.isdigit(): 
                song_num.append(num)
        return int(''.join(song_num))
    
def main()-> None:
    # Create MelonTop100 Instance
    melon : MelonTop100 = MelonTop100()
    
    # Run Method
    melon.run()
    
if __name__ == '__main__':
    main()   