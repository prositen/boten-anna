from functools import lru_cache
from plugins.restaurants.common import Foodora, add_restaurant

__author__ = 'anna'


@add_restaurant
class Zocalo(Foodora):
    url = "https://www.foodora.se/restaurant/s7ml/zocalo"

    @staticmethod
    def name():
        return "Zocalo"

    @staticmethod
    def minutes():
        return 5

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(exclude_headers=["Dryck"])
