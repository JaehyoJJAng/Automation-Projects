import os

def html_maker(file_name:str,file_path:str)-> None:
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    html_text : str = '<h1>HTML 생성하기</h1>'
    with open(os.path.join(file_path,file_name)) as fp:
        fp.write(html_text)

def main():
    file_name : str = 'index.html'
    file_path : str = 'html/'
    
    html_maker(file_name=file_name,file_path=file_path)

if __name__ == '__main__':
    main()    