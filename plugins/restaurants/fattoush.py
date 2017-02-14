from functools import lru_cache
from plugins.restaurants.common import Foodora, add_restaurant

__author__ = 'anna'


@add_restaurant
class Fattoush(Foodora):
    url = "https://www.foodora.se/restaurant/s0ya/fattoush"

    @staticmethod
    def name():
        return "Fattoush"

    @staticmethod
    def distance():
        return 8

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(exclude_headers=["Dryck"])