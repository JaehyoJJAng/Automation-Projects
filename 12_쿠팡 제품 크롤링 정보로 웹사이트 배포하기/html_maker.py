from datetime import datetime
from src.main import Coupang
from typing import Dict,List,Union
import os
import environ
import paramiko

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
            html_main_text += f"<a href='{data['link']}' target='_blank'><div class='image main'><img src='{data['thumbnail']}' alt='' /></div></a><p><h2>{data['prod_count']}위: {data['title']}</h2><b>가격 : {data['price']}원<b><br>평점 : {data['rating']}<br></b>리뷰 수 : {data['reviews']}</b><br></p>"

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

def get_env(env_file:str)-> environ.Env:
    env : environ.Env = environ.Env(DEBUG=(bool,False))
    environ.Env.read_env(env_file)
    return env    

def sftp_to_gcp(p_key:str,host:str,user:str,file_name:str)-> None:
    try:
        # Private Key
        key : paramiko.RSAKey = paramiko.RSAKey.from_private_key_file(p_key)

        # Create SSHClient Instance
        conn : paramiko.SSHClient = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(hostname=host,username=user,pkey=key)

        # Create SFTP instance
        sftp : paramiko.SFTPClient = conn.open_sftp()
        sftp.put(file_name,'/home/wogy12395/github/docker-projects/35_쿠팡 제품 크롤링 정보로 웹사이트 배포하기(Nginx)/myweb/index.html')	

        # sftp close
        sftp.close()

        # conn close
        conn.close()
        
        # Print
        print('파일 복사에 성공하였습니다!')
    except Exception as e:
        print(f'파일 복사 실패!\n:{e}')

def main():
    # Create Coupang Instance
    coupang : Coupang = Coupang()
    
    # File Path
    file_path : str = '/Users/jaehyolee/git/Inflearn-실습으로 끝장내는 파이썬 자동화 프로젝트/12_쿠팡 제품 크롤링 정보로 웹사이트 배포하기/html5up-massively'
            
    # File Name
    file_name : str = os.path.join(file_path,'index.html')
    
    # Create New Html
    html_maker(file_name=file_name,file_path=file_path,coupang=coupang)
    
    # Get Env
    env : environ.Env = get_env(env_file='ssh.env')
    
    # Copy ./html5up-massively/index.html File To GCP/myweb/index.html
    sftp_to_gcp(p_key='/Users/jaehyolee/.ssh/rsa-gcp-key',host=env('host'),user=env('user'),file_name=file_name)

if __name__ == '__main__':
    main()    