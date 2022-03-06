import requests
from bs4 import BeautifulSoup
import os
import json
import pandas as pd

link = 'https://store.steampowered.com/search/results'
term = input('Enter game you want search: ')
head = {'cookie': 'sessionid=cd46137aee87759ca68f1347'}

try:
    os.mkdir('resultfile')
except FileExistsError:
    pass


def get_pagination():
    param = {
        'term': term,
        'page': 1,
    }

    req = requests.get(link, headers=head, params=param)
    soup = BeautifulSoup(req.text, 'html.parser')
    page_item = soup.find('div', 'search_pagination_right').find_all('a')

    try:
        total_item = int(page_item[4].text)
    except Exception:
        pass
        try:
            total_item = int(page_item[3].text)
        except Exception:
            pass
            try:
                total_item = int(page_item[2].text)
            except Exception:
                pass
    return 1 + total_item


def scrap():
    count = 0
    datas = []

    for j in range(1, get_pagination()):
        param = {
            'term': term,
            'page': j,
        }
        req = requests.get(link, params=param, headers=head)
        soup = BeautifulSoup(req.text, 'html.parser')
        conten = soup.find('div', {'id': 'search_resultsRows'}).find_all('a')

        for i in conten:
            url = i['href']
            title = i.find('div', 'col search_name ellipsis').text.strip().replace('\n', ' ')
            try:
                price = i.find('div', 'col search_price responsive_secondrow').text.strip()
            except Exception:
                price = 'discount from ' + i.find('span', {'style': 'color: #888888;'}).text.replace(' ', '.') + ' to ' + i.find('div', 'col search_price discounted responsive_secondrow').find('br').next_sibling.strip() + f" ({i.find('div', 'col search_discount responsive_secondrow').text.replace('-', '').strip()})"
            if price == '':
                price = 'none'

            release = i.find('div', 'col search_released responsive_secondrow').text
            if release == '':
                release = 'none'

            data = {
                'title': title,
                'price': price,
                'release': release,
                'link': url
            }
            datas.append(data)

            count += 1
            print(f'{count}. {title}. released: {release}. price: {price} . link: {url}')

    with open(f'resultfile/json_data_{term}.json', 'w+') as outfile:
        json.dump(datas, outfile)

    df = pd.DataFrame(datas)
    df.to_csv(f'resultfile/csv data {term}.csv', index=False)
    df.to_excel(f'resultfile/excel data {term}.xlsx', index=False)
    print('all data was created')


def run():
    get_pagination()
    scrap()


run()
