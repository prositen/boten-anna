from functools import lru_cache

import requests
from bs4 import BeautifulSoup

from plugins.restaurants.common import add_restaurant, Lunch, Item


@add_restaurant
class Sabai(Lunch):
    url = 'http://www.sabaisoong.se/lunch/'

    @staticmethod
    def name():
        return 'Sabai'

    @staticmethod
    def minutes():
        return 11

    @staticmethod
    def nickname():
        return ["Thaien"]

    @lru_cache(32)
    def get(self, year, month, day):
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, 'lxml')

        menu_items = []
        headers = soup.find_all('h4')
        for item in headers:
            desc = ''
            name = item.get_text().strip()
            while item.next_sibling is not None:
                item = item.next_sibling
                tag_name = item.name
                if tag_name == 'h4':
                    break
                elif tag_name is None:
                    continue
                else:
                    desc = item.get_text().strip()
                    if not desc:
                        continue
            if name:
                menu_items.append(Item(name=name,
                                       desc=desc))
        return menu_items
