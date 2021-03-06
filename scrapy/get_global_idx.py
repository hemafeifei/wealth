
import pandas as pd
# import numpy as np
# from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
import time
import os

# chrome_path = '/Users/weizheng/PycharmProjects/tickets/chromedriver'
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_path = '/home/centos/football/chromedriver'

url = 'https://markets.businessinsider.com/indices'
today = str(datetime.now())[:16]
workday_utc0 = str(datetime.now() - timedelta(hours=24))[:10]

idx_path = '/home/centos/WEM/sec_data/'
idx_fn = 'idx_' + workday_utc0 + '.txt'

def get_soup(url):
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options)
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    driver.quit()
    display.stop()
    return soup

cols = ['index_name', 'country', 'close', 'open', 'change', 'change_pct',
       'tm_raw', 'dt_raw', 'change_3mth', 'change_6mth', 'change_ytd', 'change_12mth']
def get_global_idx(url):
    soup = get_soup(url)
    table = soup.find('table', {'class':'table instruments'})
    result_table = []
    for tr in table.find_all('tr'):
        if len(tr.find_all('td')) > 0:
            row = []
            for td in tr.find_all('td'):
                txt = td.get_text().strip()
                element = txt.split('\n')
                row.extend(element)
            result_table.append(row)
    df = pd.DataFrame(result_table, columns=cols)
    df['updated'] = today
    df['std_workday'] = workday_utc0
    df = df.drop(['tm_raw', 'dt_raw'], axis=1)
    df = df.loc[df['index_name'].isin(['Dow Jones', 'NASDAQ 100', 'S&P 500', 'FTSE 100', 'DAX', 'CAC 40',
                    'NIKKEI 225', 'Hang Seng', 'Shanghai Composite'])].reset_index(drop=True)
    return df


idx_data = get_global_idx(url)

if not os.path.exists(idx_path + idx_fn):
    print(today, "Update")
    print(idx_data.shape)
    print("****"*5)
    idx_data.to_csv(idx_path + idx_fn, index=False, encoding='utf8')
else:
    print('Breake - file existes')
    print("====" * 5)

