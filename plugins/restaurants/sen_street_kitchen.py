from functools import lru_cache
from plugins.restaurants.common import Foodora, add_restaurant

__author__ = 'anna'


@add_restaurant
class SenStreetKitchen(Foodora):
    url = "https://www.foodora.se/restaurant/s6lx/sen-street-kitchen"

    @staticmethod
    def name():
        return "Sen Street Kitchen"

    @staticmethod
    def minutes():
        return 8

    @staticmethod
    def nickname():
        return ['Sen', 'Sen street']

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(exclude_headers=["Smårätter", "Dryck"])
