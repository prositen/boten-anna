from functools import lru_cache
from plugins.restaurants.common import add_restaurant, Foodora, Item

__author__ = 'anna'


@add_restaurant
class Wiggos(Foodora):
    url = "https://www.foodora.se/restaurant/s1qa/wiggo-wraps-hornstull"

    @staticmethod
    def name():
        return "Wiggos"

    @staticmethod
    def minutes():
        return 10

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(exclude_headers=["Dryck - Stilla", "Dryck - kolsyrad"])
