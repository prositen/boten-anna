from functools import lru_cache

from plugins.restaurants.common import add_restaurant, Kvartersmenyn


@add_restaurant
class Sabis(Kvartersmenyn):
    url = 'http://www.kvartersmenyn.se/rest/13906'

    @staticmethod
    def name():
        return 'Sabis'

    @staticmethod
    def minutes():
        return 7
