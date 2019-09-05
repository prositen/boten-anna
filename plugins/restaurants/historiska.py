import datetime
import re
from functools import lru_cache

import requests
from bs4 import BeautifulSoup

from plugins.restaurants.common import add_restaurant, Lunch, Item


@add_restaurant
class Historiska(Lunch):
    url = 'https://historiska.se/kalendarium'

    @staticmethod
    def name():
        return 'Historiska'

    @staticmethod
    def minutes():
        return 5

    @lru_cache(32)
    def get(self, year, month, day):
        isolocal = datetime.date(year, month, day).isocalendar()
        week = isolocal[1]
        url = '{url}/{year}/{month:02}/{day:02}/dagens-lunch-v{week}-{year}/' \
            .format(url=self.url,
                    year=year,
                    month=month,
                    day=day,
                    week=week)

        result = requests.get(url)
        if result.status_code == 404:
            return []
        menu_items = []
        soup = BeautifulSoup(result.content, 'lxml')
        headers = soup.find("div", {"class": "post-content"}).findAll("h2")
        day_re = re.compile(r'.* (\d+) \w+')
        for header in headers:
            day_result = day_re.match(header.get_text())
            if day_result is not None:
                if day == int(day_result.group(1)):
                    day_found = True
                else:
                    day_found = False
            else:
                day_found = True

            if day_found:
                items = header.next_sibling.next_sibling.findAll('li')
                for item in items:
                    name = item.get_text().strip()
                    menu_items.append(Item(name))

        return menu_items
