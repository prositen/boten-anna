from plugins.restaurants.common import add_restaurant, Lunch, Item


@add_restaurant
class DCCatering(Lunch):
    url = 'http://dccatering.se'

    @staticmethod
    def name():
        return 'DC Catering'

    @staticmethod
    def minutes():
        return 2

    def get(self, year, month, day):
        return [
            Item('Pasta Carbonara', cost=90),
            Item('Sushi'),
            Item('Yakiniku', cost=90)
        ]

    @staticmethod
    def nickname():
        return ['dc', 'pasta']