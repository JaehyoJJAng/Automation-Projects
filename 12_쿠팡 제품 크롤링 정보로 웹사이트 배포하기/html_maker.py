from datetime import datetime
from src.main import Coupang
from typing import Dict,List,Union
import os

def create_dir(file_path:str):
    if not os.path.exists(file_path):
        os.mkdir(file_path)    

def html_maker(file_name:str,file_path:str,coupang:Coupang)-> None:
    # Create Directory
    create_dir(file_path=file_path)
    
    # Crawl Data List
    data_list : List[List[Dict[str,Union[str,int,float]]]] = coupang.run()

    # Empty html_main_text
    html_main_text : str = ''
    for x in data_list:
        for data in x:              
            # Main Text
            html_main_text += f"<a href='{data['link']}' target='_blank'><div class='image main'><img src='{data['thumbnail']}' alt='' /></div></a><p><h2>{data['prod_count']}위: {data['title']}</h2><b>가격 : {data['price']}원<b>평점 : {data['rating']}<b>리뷰 수 : {data['reviews']}</b></>"

    # Title
    html_title : str = f'오늘의 {coupang.keyword}'
    
    # Product Name
    html_prod_name : str = f'오늘의 {coupang.keyword}'
    
    # Date
    html_today : str = datetime.now().strftime('%Y년 %m월 %d일')
    
    # Sub Text
    html_sub_text : str  = f'{html_today} 오늘의 {coupang.keyword} 인기상품 Top30 입니다'
    
    # HTML
    html : str = f"""
<!DOCTYPE HTML>
<!--
	Massively by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
	<head>
		<title>{html_title}</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<link rel="stylesheet" href="assets/css/main.css" />
		<noscript><link rel="stylesheet" href="assets/css/noscript.css" /></noscript>
	</head>
	<body class="is-preload">
		<!-- Wrapper -->
			<div id="wrapper">
				<!-- Header -->
					<header id="header">
						<a href="index.html" class="logo">Massively</a>
					</header>
				<!-- Main -->
					<div id="main">
						<!-- Post -->
							<section class="post">
								<header class="major">
									<span class="date">{html_today}</span>
									<h1>{html_prod_name}</h1>
									<p>{html_sub_text}</p>
								</header>
								{html_main_text}
							</section>
					</div>
				<!-- Copyright -->
					<div id="copyright">
						<ul><li>&copy; Untitled</li><li>Design: <a href="https://html5up.net">HTML5 UP</a></li></ul>
					</div>
			</div>
		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrollex.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/browser.min.js"></script>
			<script src="assets/js/breakpoints.min.js"></script>
			<script src="assets/js/util.js"></script>
			<script src="assets/js/main.js"></script>
	</body>
</html>"""
    
    # Text Write To File
    with open(os.path.join(file_path,file_name),'w') as fp:
        fp.write(html)

def main():
    # Create Coupang Instance
    coupang : Coupang = Coupang()
    
    # File Name
    file_name : str = 'index.html'
    
    # File Path
    file_path : str = 'html5up-massively'
    
    # Create New Html
    html_maker(file_name=file_name,file_path=file_path,coupang=coupang)

if __name__ == '__main__':
    main()    