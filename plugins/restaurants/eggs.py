from functools import lru_cache
from plugins.restaurants.common import Foodora, add_restaurant

__author__ = 'anna'


@add_restaurant
class Eggs(Foodora):
    url = "https://www.foodora.se/restaurant/s6bo/eggs-inc"

    @staticmethod
    def name():
        return "Eggs"

    @staticmethod
    def minutes():
        return 5

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(exclude_headers=["Äggägg", "Dessert", "Dryck", "Extra", "Äggwrap"])

