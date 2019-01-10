import pandas as pd
import numpy as np
# from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta

chrome_path = '/Users/weizheng/PycharmProjects/tickets/chromedriver'
url = 'https://qieman.com/idx-eval'
today = str(datetime.now())[:10]

def get_soup_eng_pr(url):
    driver = webdriver.Chrome(executable_path=chrome_path)
    # driver = webdriver.Firefox(executable_path=firefox_path)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    driver.close()
    return soup

soup = get_soup_eng_pr(url)


if today == soup.find("span", {'class': 'qm-header-note'}).p.get_text().split(' ')[0]:
    print("YES, today got update for {}".format(today))

    lst = []
    tbl = soup.find('div', {'class': 'flex-table__67b31'})
    # tbl_low = soup.find('div', {'class': 'flex-table-body group-LOW'})
    # tbl_mid = soup.find('div', {'class': 'flex-table-body group-MID'})
    # tbl_na = soup.find('div', {'class': 'flex-table-body group-NA'})

    for row in tbl.find_all("div", {"class": 'flex-table-row'}):
        info = [p.get_text() for p in row.find_all('p')[1:]]
        name = row.find("p")
        for i in name.find_all('span'):
            info.insert(0, i.get_text())
        lst.append(info)

    df = pd.DataFrame(lst, columns=['idx', 'name', 'pe_or_pb', 'percentile_qm', 'max_qm', 'min_qm', 'row_qm'])
    df = df.replace("--", np.nan)
    df['dt'] = today
    print(df.shape)
    df.to_csv('../data/qm_' + today + '.txt', index=False)
    print("saved file")
else:
    print("there wasn't an update for {}".format(today))

