from functools import lru_cache
from plugins.restaurants.common import add_restaurant, Foodora

__author__ = 'anna'


@add_restaurant
class Phils(Foodora):
    url = "https://www.foodora.se/restaurant/s3uc/phil-s-burger-gardet"

    @staticmethod
    def name():
        return "Phils"

    @staticmethod
    def minutes():
        return 16

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(exclude_headers=["Extras", "Dippsåser", "Dryck"])