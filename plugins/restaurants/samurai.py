import datetime
from functools import lru_cache

import requests
from bs4 import BeautifulSoup

from plugins.restaurants.common import add_restaurant, Lunch, HeaderListParser, Item


@add_restaurant
class Samurai(Lunch):
    url = 'https://www.samurai.rest/meny/'

    @staticmethod
    def name():
        return 'Samurai'

    @staticmethod
    def minutes():
        return 13

    @lru_cache(32)
    def get(self, year, month, day):
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, 'lxml')
        default_cost = 120
        weekday = datetime.datetime(year, month, day).isoweekday()

        menu_items = []
        daily_headers = soup.find_all('h4')
        for item in daily_headers:
            text = item.get_text().strip()
            if text and len(text) >= 3:
                text = text.lower()[:3]
                if self.DAYS.get(text, 0) == weekday:
                    while item.next_sibling is not None:
                        item = item.next_sibling
                        tag_name = item.name
                        if tag_name == 'h4':
                            break
                        elif tag_name is None:
                            continue
                        menu_item = item.find('strong')
                        if menu_item:
                            name = menu_item.get_text()
                            desc = item.get_text()[len(name):]
                            menu_items.append(Item(name=name,
                                                   desc=desc,
                                                   cost=default_cost))

                else:
                    continue
        for item in soup.find_all('h3'):
            if item.get_text().strip().lower() == 'veckans tips':
                while item.next_sibling is not None:
                    item = item.next_sibling
                    if item is None:
                        break
                    if item.name is None:
                        continue
                    elif item.name != 'p':
                        break
                    menu_item = item.find('strong')
                    name_cost = menu_item.get_text()
                    desc = item.get_text()[len(name_cost):]
                    words = name_cost.split(' ')
                    cost = int(words[-2])
                    name = ' '.join(words[:-2])
                    menu_items.append(Item(name=name,
                                           desc=desc,
                                           cost=cost))
        return menu_items
