from plugins.restaurants.common import NoDaily, add_restaurant, Item

__author__ = 'anna'


@add_restaurant
class LebanonMezaLounge(NoDaily):
    url = "http://www.lebanonml.com"

    @staticmethod
    def name():
        return "LebanonMezaLounge"

    @staticmethod
    def get(self, year, month, day):
        return [Item('Buffé', cost=120)]

    @staticmethod
    def distance():
        return 1

    @staticmethod
    def nickname():
        return ['Libanesen']
