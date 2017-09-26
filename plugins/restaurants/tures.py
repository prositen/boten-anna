import datetime
from functools import lru_cache
import re
from bs4 import BeautifulSoup
import requests
from plugins.restaurants.common import Lunch, Item, add_restaurant

__author__ = 'anna'


@add_restaurant
class Tures(Lunch):
    url = "http://tures.se"

    @staticmethod
    def name():
        return "Tures"

    @staticmethod
    def minutes():
        return 11

    @lru_cache(32)
    def get(self, year, month, day):
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, "html.parser")
        dagens = soup.find("div", {"class": "dagens"})
        try:
            pris = int(dagens.get_text().split()[2])
        except IndexError:
            pris = 0
        rows = dagens.findAll('li')
        menu_items = []
        for row in rows:
            name = row.get_text().strip()
            menu_items.append(Item(name, "", pris))
        return menu_items
