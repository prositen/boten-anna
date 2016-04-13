import datetime
from plugins.restaurants.common import Lunch, Item, add_restaurant

__author__ = 'anna'


@add_restaurant
class Subway(Lunch):
    url = "http://www.subway.se"

    SUBS = ['American Steakhouse Melt',
            'Subway Melt',
            'Spicy Italian',
            'Rostbiff',
            'Tonfisk',
            'Subway Club',
            'Italian B.M.T.']

    @staticmethod
    def name():
        return "Subway"

    @staticmethod
    def minutes():
        return 7

    def get(self, year, month, day):
        date = datetime.datetime(year, month, day)
        return [Item("Sub of the day (15 cm): " + self.SUBS[date.isoweekday()], cost=35)]
