from typing import Dict
import os
import json

def get_headers():
    with open('src/headers/headers.json','r') as fp:
        headers : Dict[str,str] = json.loads(fp.read())    
    try:
        return headers
    except: 
        raise EnvironmentError()