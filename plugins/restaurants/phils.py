from functools import lru_cache
from bs4 import BeautifulSoup
import requests
from plugins.restaurants.common import Lunch, Item, add_restaurant

__author__ = 'anna'


@add_restaurant
class Phils(Lunch):
    url = "http://www.philsburger.se/#pmeny"

    @staticmethod
    def name():
        return "Phils"

    @staticmethod
    def minutes():
        return 10

    @lru_cache(32)
    def get(self, year, month, day):
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, "html.parser")
        menu = soup.find("h4", {"class": "items-title"})
        menu_items = []
        n = menu.nextSibling
        while n is not None and n.name != 'div':
            n = n.nextSibling
        for item in n.findAll("div", {"class": "food"}):
            name_elem = item.find("h4", {"class": "title"})
            desc = name_elem.parent.nextSibling.strip()
            name = name_elem.next.strip()
            menu_items.append(Item(name, desc))
        return menu_items
