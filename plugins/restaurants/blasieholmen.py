import datetime
from functools import lru_cache
import re
from bs4 import BeautifulSoup
import requests
from plugins.restaurants.common import Lunch, Item, add_restaurant

__author__ = 'anna'


@add_restaurant
class Blasieholmen(Lunch):
    url = "http://blasieholmenrestaurang.se/lunch/"

    @staticmethod
    def name():
        return "Blasieholmen"

    @staticmethod
    def minutes():
        return 2

    @lru_cache(32)
    def get(self, year, month, day):
        day_header = re.compile(r'(Måndag|Tisdag|Onsdag|Torsdag|Fredag)', re.IGNORECASE)
        isocal = datetime.date(year, month, day).isocalendar()
        weekday = isocal[2]
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, "html.parser")
        paragraphs = soup.find("div", {"class": "modal-body"}).findAll('p')
        found_day = False
        menu_items = []
        for p in paragraphs:
            p_text = p.get_text().strip()
            day_result = day_header.match(p_text)
            if day_result:
                if found_day:
                    found_day = False
                elif weekday == self.DAYS[day_result.group(1).lower()[:3]]:
                    found_day = True
            else:
                if found_day:
                    menu_items.append(Item("Buffé: " + p.get_text(), cost=105))
        return menu_items
