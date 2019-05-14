import datetime
from functools import lru_cache

import requests
from bs4 import BeautifulSoup, Tag

from plugins.restaurants.common import add_restaurant, Lunch, Item


@add_restaurant
class Cassi(Lunch):

    url = 'http://www.cassi.se/dagens-r%C3%A4tt-15279665'

    @staticmethod
    def name():
        return 'Cassi'

    @staticmethod
    def minutes():
        return 8

    @lru_cache(32)
    def get(self, year, month, day):
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, 'lxml')
        menu_items = []
        isocal = datetime.date(year, month, day).isocalendar()
        weekday = isocal[2]

        for elem in soup.find_all('strong'):
            day_header = elem.get_text().strip()
            if len(day_header) > 6 and self.DAYS.get(day_header[0:3].lower(), -1) == weekday:
                for item in elem.next_siblings:
                    cost = 120
                    food = str(item).strip()
                    if not len(food) or food == '<br/>':
                        continue
                    if food.startswith('<strong>'):
                        break
                    if food.endswith(':-'):
                        spl = food.split(' ')
                        cost = int(spl[-1][:-2], 10)
                        food = ' '.join(spl[:-1])
                    menu_items.append(Item(name=food, cost = cost))



        return menu_items
