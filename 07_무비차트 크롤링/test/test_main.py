from __init__ import MovieChart
from typing import Dict,List,Union
import requests as rq
import unittest

class MovieChartTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.movie : MovieChart = MovieChart()
    
    def test_get_soup_obj(self):
        with rq.Session() as session:
            with session.get(url=self.movie._base_url,headers=self.movie._headers) as response:
                soup = self.movie.get_soup_obj(response=response)
                
                page_check : bool = False
                if '무비차트' in str(soup.text):
                    page_check = True
        self.assertTrue(page_check)
    
    def test_get_movie_length(self):
        with rq.Session() as session:
            with session.get(url=self.movie._base_url,headers=self.movie._headers) as response:
                soup = self.movie.get_soup_obj(response=response)                
                tag : str = 'div.wrap-movie-chart div.sect-movie-chart > ol > li'
                movie_length : int = self.movie.get_movie_length(soup=soup,tag=tag)
        self.assertEqual(movie_length,19)
    
    def test_get_movie_content(self):
        with rq.Session() as session:
            with session.get(url=self.movie._base_url,headers=self.movie._headers) as response:
                soup = self.movie.get_soup_obj(response=response)                
                tag : str = 'div.wrap-movie-chart div.sect-movie-chart > ol > li'
                movie_length : int = self.movie.get_movie_length(soup=soup,tag=tag)
                results: List[Dict[str,Union[str,int,float]]] = self.movie.get_movie_content(soup=soup,movie_length=movie_length,tag=tag)
        self.assertEqual(len(results),19)        

if __name__ == '__main__':
    unittest.main()