from functools import lru_cache
from plugins.restaurants.common import Foodora, add_restaurant

__author__ = 'anna'


@add_restaurant
class Panini(Foodora):
    url = "https://www.foodora.se/restaurant/hk5l/panini-hamngatan-15"

    @staticmethod
    def name():
        return "Panini"

    @staticmethod
    def minutes():
        return 7

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(exclude_headers=["Mindre måltider", "Dryck"])
