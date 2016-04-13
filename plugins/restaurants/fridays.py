import datetime
from functools import lru_cache
from plugins.restaurants.common import Lunch, Item, add_restaurant

__author__ = 'anna'


@add_restaurant
class Fridays(Lunch):
    SPECIAL = [("Premium Burgers", 119),
               ("Ribs Ribs Ribs", 119),
               ("Steaks", 199)]

    url = "https://fridays.se/"

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
        return [Item("Bacon Cheeseburger", cost=99), Item("Chicken Caesar Salad", cost=99),
                Item("Chicken Finger BLT Sandwich", cost=99), Item("Crispy Chicken Tenders", cost=99),
                Item("Lemon Basil Salad", cost=99), Item("Buffalo Chicken Sandwich", cost=99),
                Item("Jack Daniel's Burger", cost=99), Item("Romesco Grilled Vegetable Pasta", cost=99),
                Item("Jack Daniel's Chicken Burger", cost=99), Item("Fridays Finest Falafel", cost=99),
                Item("Tennessee BBQ Pulled Pork Sandwich", cost=99), Item("Creamy Buffalo Chicken Pasta", cost=99),
                Item("Weekly Special: {0}".format(self.SPECIAL[week][0]), cost=self.special[week][1])]
