from plugins.restaurants.common import NoDaily, add_restaurant

__author__ = 'anna'


@add_restaurant
class Vapiano(NoDaily):
    url = "http://se.vapiano.com/sv/meny/specials/"

    @staticmethod
    def name():
        return "Vapiano"

    @staticmethod
    def minutes():
        return 9

    @staticmethod
    def nickname():
        return ['Vappe']
