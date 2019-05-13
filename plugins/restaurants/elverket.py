import datetime
from functools import lru_cache

import requests
from bs4 import BeautifulSoup

from plugins.restaurants.common import add_restaurant, Lunch, HeaderListParser, Item


@add_restaurant
class Elverket(Lunch, HeaderListParser):
    url = 'https://www.brasserieelverket.se/lunch/'

    @staticmethod
    def name():
        return 'Elverket'

    @staticmethod
    def minutes():
        return 7

    @lru_cache(32)
    def get(self, year, month, day):
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, 'lxml')
        menu_items = []
        lunch_elem = soup.find('div', {'id': 'lunch'})

        items = lunch_elem.find_all('p')
        for item in items:
            name = item.find('strong')
            if name:
                desc = item.find('br')
                if desc:
                    desc = desc.nextSibling
                cost = item.find('span')

            else:
                item_info = list(item.next_siblings)
                if len(item_info) > 3:
                    name = item_info[0]
                    desc = item_info[2]
                    cost = item_info[3]
                else:
                    continue

            name = name.get_text().strip()
            desc = str(desc).strip() if desc else ''
            cost = int(cost.get_text().strip(), 10)

            menu_items.append(Item(name, desc, cost))

        return menu_items



