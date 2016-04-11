import datetime
from functools import lru_cache
from plugins.restaurants.common import Lunch, Item, add_restaurant

__author__ = 'anna'


@add_restaurant
class Fridays(Lunch):
    SPECIAL = ["Premium Burgers",
               "Ribs Ribs Ribs",
               "Steaks"]

    @staticmethod
    def name():
        return "Fridays"

    @staticmethod
    def minutes():
        return 1

    @lru_cache(32)
    def get(self, year, month, day):
        isocal = datetime.date(year, month, day).isocalendar()
        week = isocal[1] % 3
        return [Item("Bacon Cheeseburger"), Item("Chicken Caesar Salad"), Item("Chicken Finger BLT Sandwich"),
                Item("Crispy Chicken Tenders"), Item("Lemon Basil Salad"), Item("Buffalo Chicken Sandwich"),
                Item("Jack Daniel's Burger"), Item("Romesco Grilled Vegetable Pasta"),
                Item("Jack Daniel's Chicken Burger"), Item("Fridays Finest Falafel"),
                Item("Tennessee BBQ Pulled Pork Sandwich"), Item("Creamy Buffalo Chicken Pasta"),
                Item("Weekly Special: {0}".format(self.SPECIAL[week]))]
