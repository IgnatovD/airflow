import time
import requests
from bs4 import BeautifulSoup
from random import choice



def get_proxy() -> dict:
    html = requests.get('https://free-proxy-list.net/').text
    soup = BeautifulSoup(html, 'lxml')

    trs = soup.find('table', class_='table table-striped table-bordered').find_all('tr')[1:300]

    proxies = []
    for tr in trs:
        tds = tr.find_all('td')
        # выберем только https
        if tds[6].text.strip() == 'no':
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            schema = 'https' if 'yes' in tds[6].text.strip() else 'http'
            proxy = {'schema': schema, 'address': ip + ':' + port}
            proxies.append(proxy)
    return choice(proxies)


def request(url: str) -> requests.models.Response:
    p = get_proxy()
    proxy = {p['schema']: p['address']}
    r = requests.get(url, proxies=proxy, timeout=5)
    return r


def get_html(url: str) -> str:
    r = request(url)
    if r.ok:
        return r.text
    else:
        print(r.status_code)
        while not r.ok:
            time.sleep(30)
            r = request(url)
        return r.text