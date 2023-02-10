from typing import Dict
import os
import json

def get_headers(key:str):
    with open('headers/headers.json','r') as fp:
        headers : Dict[str,str] = json.loads(fp.read())    
    try:
        return headers[key]
    except: 
        raise EnvironmentError(f'Set the {key}')