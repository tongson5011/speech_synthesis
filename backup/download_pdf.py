import requests
import os
from concurrent.futures import ThreadPoolExecutor

PATH = os.path.dirname(os.path.abspath(__file__))
img = os.path.join(PATH,'img')
os.makedirs(img, exist_ok=True)


cookies = {
    'NID': '511=hmMW5nZyqtg628kHOTDsjDqZ_tM1OmxADFyFWB8wbQNwrhz5V1PHHiIj-AcYsYqE-ysu5s-4f-zvy6J48yz7MjFBdM8UhCpy6LYw_ZcnR-WNFh4cd73pfZ2owALbxilOZMF6oHvr5DgtyU6r225Raniy8HRH3OuYQSHAGrBZr8g',
}

headers = {
    'authority': 'drive.google.com',
    'accept': '*/*',
    'accept-language': 'en',
    'referer': 'https://drive.google.com/',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}

i = 0
def download_pdf(stt=0):
    params = {
    'ck': 'drive',
    'ds': 'APznzaZKuQCK6_ny1GcdlqKbPgAmzs_vOmpHdBGWiQbUNuFl5nNcSY_Cv9OSpRvf2SICg18v0BUjmJFSVC4n2QKB43c9NNF-SK0vrmwquUVx63iJyPgJtnQ72OLydeeBqQmrEOO9kGcbUQNpgLcQlr6DxEWQeLWA4sQS8SxO9DmSVKRcvsthq46wesk81LGLhNnQX0ORWtuSN483gy5m1LCWs57AvI6tDDQwLHv5V3XixGRRk9FmtYLQ71gub0hjuXkLb2Q3DXjD0b0brHRNQoYn4VlEhUrX_pp6dmpDML3Wiyomf9Q-ddezmtiTQcFpgIdmJQTQLTCM6kCW4b1TisBg0aA2eB99OgVJ9UwdcDLGC3iIU9noaHaF3cbn5pPtjlG6IJr9YAj59I5O7OeZVstiytnqLMwQrQ==',
    'authuser': '0',
    'page': f'{stt}',
    'skiphighlight': 'true',
    'w': '1600',
    'webp': 'true',
    }
    response = requests.get('https://drive.google.com/viewer2/prod-03/img', params=params, cookies=cookies, headers=headers)
    if response.status_code == 200 or  response.status_code == 201:
        with open(f'img\img{stt}.png', 'wb') as f:
            f.write(response.content)
        print(f'save img{stt} was success' )
        return True
    else:
        print(f'save img{stt} was failed' )
        return False

list_process = []
with ThreadPoolExecutor() as executor:
    for stt in range(0,682):
        process = executor.submit(download_pdf, *[stt])
        print(stt)
        list_process.append(process)