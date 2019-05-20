from functools import lru_cache

from plugins.restaurants.common import add_restaurant, Foodora


@add_restaurant
class EastIndia(Foodora):
    url = 'https://www.foodora.se/restaurant/s8jx/east-india'

    @staticmethod
    def name():
        return 'East India'

    @staticmethod
    def minutes():
        return 10

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(include_headers=['Dagens lunch'])