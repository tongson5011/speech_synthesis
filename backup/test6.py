import requests
from requests_html import HTML
from urllib.parse import urljoin

cookies = {
    'ASPSESSIONIDAGQBQRQB': 'NHIBCCDACJNCPPGFIBGGIIPB',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
    'Connection': 'keep-alive',
    # 'Cookie': 'ASPSESSIONIDAGQBQRQB=NHIBCCDACJNCPPGFIBGGIIPB',
    'Referer': 'https://baotri.911.com.vn/911group/desktopaccept/view/11798/FEA645EE-BBD4-40FC-81D9-EC6EB811B32A',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61',
    'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get(
    'https://baotri.911.com.vn/911group/choosestaff/view/11798/FEA645EE-BBD4-40FC-81D9-EC6EB811B32A/04-0321/desktopaccept/addstaff/0/0/',
    cookies=cookies,
    headers=headers,
)
baseURL = 'https://baotri.911.com.vn/'
if response.status_code == 200:
    data_html = HTML(html=response.text)
    data_link = data_html.find('a', first=True)
    if data_link:
        user_link = urljoin(baseURL, data_link.attrs['href'])
        print(user_link)
        r2 = response = requests.get(user_link,  cookies=cookies, headers=headers)
        