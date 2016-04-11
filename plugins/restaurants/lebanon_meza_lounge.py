from plugins.restaurants.common import NoDaily, add_restaurant

__author__ = 'anna'


@add_restaurant
class LebanonMezaLounge(NoDaily):
    url = "http://www.lebanonml.com"

    @staticmethod
    def name():
        return "LebanonMezaLounge"

    @staticmethod
    def distance():
        return 1

    @staticmethod
    def nickname():
        return ['Libanesen']
