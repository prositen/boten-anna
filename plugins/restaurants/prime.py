from functools import lru_cache
from plugins.restaurants.common import Foodora, add_restaurant

__author__ = 'anna'


@add_restaurant
class Prime(Foodora):
    url = "https://www.foodora.se/restaurant/s8ci/prime-burger-birger-jarlsgatan"

    @staticmethod
    def name():
        return "Prime"

    @staticmethod
    def minutes():
        return 15

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(exclude_headers=["Side Orders", "Milkshakes", "Soft Drinks"])

