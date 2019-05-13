from functools import lru_cache
from plugins.restaurants.common import Foodora, add_restaurant

__author__ = 'anna'


@add_restaurant
class Panini(Foodora):
    url = "https://www.foodora.se/restaurant/s1qg/panini-garnisonen"

    @staticmethod
    def name():
        return "Panini"

    @staticmethod
    def minutes():
        return 2

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(exclude_headers=["Mindre måltider", "Extra dressing", "Dryck"])
