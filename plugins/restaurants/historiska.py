from plugins.restaurants.common import add_restaurant, Lunch


@add_restaurant
class Historiska(Lunch):

    url = ''
    @staticmethod
    def name():
        return 'Historiska'

    @staticmethod
    def minutes():
        return 5