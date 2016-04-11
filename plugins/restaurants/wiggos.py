from functools import lru_cache
from bs4 import BeautifulSoup
import requests
from plugins.restaurants.common import Lunch, HeaderListParser, add_restaurant

__author__ = 'anna'


@add_restaurant
class Wiggos(Lunch, HeaderListParser):
    url = "http://wiggowraps.se/menus/huvudmeny/"

    @staticmethod
    def name():
        return "Wiggos"

    @staticmethod
    def minutes():
        return 5

    def parse_page(self, soup=None,
                   header_elem="h3", header_elem_class="None",
                   exclude_headers=None,
                   food_wrapper=None, food_wrapper_class=None,
                   name_elem=None, name_class=None,
                   desc_elem=None, desc_class=None):
        return super(Wiggos, self).parse_page(soup,
                                              header_elem="h2", exclude_headers=["Snacks", "Dryck"],
                                              food_wrapper="span", food_wrapper_class="foodmenuwrap",
                                              name_elem="span", name_class="foodmenudesc",
                                              desc_elem="span", desc_class="fooddesc")

    @lru_cache(32)
    def get(self, year, month, day):
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, "html.parser")
        content = soup.find("div", {"class": "entry-content"})
        return self.parse_page(content)
