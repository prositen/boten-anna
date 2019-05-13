from plugins.restaurants.common import add_restaurant, Lunch, Item


@add_restaurant
class KMarkt(Lunch):
    @staticmethod
    def name():
        return "K-märkt"

    @staticmethod
    def minutes():
        return 2

    def get(self, year, month, day):
        return [Item('Buffé')]