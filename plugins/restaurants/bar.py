import datetime
from functools import lru_cache
from plugins.restaurants.common import Lunch, Item, add_restaurant

__author__ = 'anna'


@add_restaurant
class Bar(Lunch):

    url = "https://restaurangbar.se/?redirect=true"

    @staticmethod
    def name():
        return "B.A.R"

    @staticmethod
    def nickname():
        return ["BAR"]

    @staticmethod
    def minutes():
        return 8

    @lru_cache(32)
    def get(self, year, month, day):
        return [Item("Gratinerade kammusslor", cost=180), Item("Toast Skagen \"Royal\"", cost=250),
                Item("King prawns", cost=170), Item("Grillad Laxsashimi", cost=175),
                Item("Vattenmeloncocktail", cost=165), Item("Ceviche", cost=180),
                Item("Grillad majstortilla, havsabborre", cost=160), Item("Frasig rödtungasallad", cost=150),
                Item("Charkuterier från Millert & Dahlén", cost=140), Item("Havstallrik", cost=175),
                Item("30 g löjrom, Junkön", cost=180),
                Item("Steak tartar", cost=150), Item("Rostad pumpa", cost=175), Item("Moules Frites", cost=190),
                Item("Fisk & skaldjursgryta", cost=195), Item("Fish n' Chips", cost=185), Item("Sandwich", cost=165),
                Item("Take away: Räksallad", cost=105),
                Item("Take away: Dagens husman", cost=96),
                Item("Take away: Sandwich", cost=155),
                Item("Take away: Fish n' Chips", cost=165),
                Item("Take away: Fisk och skaldjursgryta", cost=175),
                Item("Take away: Rostad pumpa", cost=155)]
