import re
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from utils.tools import get_proxy, request, get_html



#TODO exchange name function
def get_df_pet() -> pd.DataFrame:
    dt = datetime.now()

    url = 'https://pogoda.mail.ru/prognoz/moskva/24hours/'
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    temperature = \
    soup.find('div', class_='p-forecast__item p-forecast__item_temperature p-forecast__grid-content').find_all('span')[
        -2].text
    temperature = float(re.search(r'\w*\d+\w*', temperature).group())

    return pd.DataFrame([{'time': dt, 'temperature': temperature}])