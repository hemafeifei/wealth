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

url = 'http://www.boc.cn/sourcedb/whpj/index.html'
today = str(datetime.now())[:10]
fx_path = '../fx_data/'
fx_fn = 'fx_' + today + '.txt'

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


def get_fx(url):
    soup = get_soup(url)
    odd_table = soup.find_all('table')[-3]
    table = []
    for tr in odd_table.find_all('tr')[1:]:
        row = tr.get_text().split('\n')
        table.append(row)

    df = pd.DataFrame(table, columns=['N0', 'name', 'current_buy', 'cash_buy', 'current_sell', 'cash_sell',
                                'boc_price', 'date', 'time', 'N99'])
    df = df.drop(['N0', 'N99'], axis=1)
    df = df.loc[df.name.isin(['澳大利亚元', '加拿大元', '瑞士法郎', '欧元', '英镑',
           '港币', '日元', '韩国元', '新加坡元', '泰国铢', '土耳其里拉', '美元', '南非兰特'])].reset_index(drop=True)
    return df


fx_data = get_fx(url)
if fx_data['date'][0] == today:
    if not os.path.exists(fx_path + fx_fn):
        print(today, "Update")
        fx_data.to_csv(fx_path + fx_fn, index=False)
    else:
        print('Breake - file existes')
else:
    print('Break - not today')
    print(today)
    print(fx_data.shape)
    print(fx_data['date'][0])
