from functools import lru_cache

from plugins.restaurants.common import add_restaurant, Foodora


@add_restaurant
class Bap(Foodora):
    url = 'https://www.foodora.se/restaurant/s0es/bap-burgers-pastrami'

    @staticmethod
    def name():
        return 'BAP'

    @staticmethod
    def minutes():
        return 15

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(exclude_headers=['Sides', 'Pastrami', 'Dryck'])

