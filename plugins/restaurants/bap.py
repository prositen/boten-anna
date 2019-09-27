from functools import lru_cache

import requests
from bs4 import BeautifulSoup, Tag

from plugins.restaurants.common import add_restaurant, Item, Kvartersmenyn


@add_restaurant
class Bap(Kvartersmenyn):
    url = 'http://bap.kvartersmenyn.se/'

    @staticmethod
    def name():
        return 'BAP'

    @staticmethod
    def minutes():
        return 15

    @lru_cache(32)
    def get(self, year, month, day):
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, 'lxml')
        menu_items = []

        menu = soup.find('div', {'class': 'meny'})
        name = ''
        desc = ''
        for item in menu.children:
            if isinstance(item, Tag):
                t = item.get_text().strip()
                if len(t) < 2:
                    continue
                if t.startswith('TILLVAL'):
                    break
                name = t
                desc = ''
            else:
                if name:
                    d, cost = self.parse_price(item)
                    desc += d
                    if cost:
                        menu_items.append(Item(name=name,
                                               desc=desc,
                                               cost=cost))

        return menu_items