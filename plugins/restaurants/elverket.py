import datetime
import re
from functools import lru_cache

import requests
from bs4 import BeautifulSoup

from plugins.restaurants.common import add_restaurant, Lunch, HeaderListParser, Item


@add_restaurant
class Elverket(Lunch, HeaderListParser):
    url = 'https://www.brasserieelverket.se/#Dlunch'

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
        lunch_elem = soup.find('div', {'id': 'Dlunch', 'class': 'x-section'})

        items = lunch_elem.find_all('div', {'class': 'x-column'})
        for item in items:
            i = item.find_all('p')
            if len(i) == 3:
                name = i[0].get_text().strip()
                desc = i[1].get_text().strip()
                cost = i[2].get_text().strip()
                if cost:
                    cost = int(re.sub(r'\D', '', cost), 10)
                menu_items.append(Item(name, desc, cost))

        return menu_items



