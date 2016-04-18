import datetime
from functools import lru_cache
from plugins.restaurants.common import Lunch, Item, add_restaurant, NoDaily

__author__ = 'anna'


@add_restaurant
class Locals(NoDaily):

    url = "http://localsfood.se/Locals%20Meny.pdf"

    @staticmethod
    def name():
        return "Locals"

    @staticmethod
    def minutes():
        return 1

    @lru_cache(32)
    def get(self, year, month, day):
        return [Item("Kycklingfilé", "med råris & currysås", 99),
                Item("Kycklingfilé", "med pasta & mangochili/yoghurt", 99),
                Item("Kycklingfilé", "med bulgur & thaisås", 99),
                Item("Kycklingfilé", "med potatis & ratatouille", 99),
                Item("Kycklingfilé", "med bönor & bulgur & senaps/yoghurt", 99),
                Item("Vegetarisk chili", "med råris", 95),
                Item("Vegetarisk chili", "med bulgur", 95),
                Item("Vegetarisk chili", "med pasta", 95),
                Item("Pulled beef", "med råris & marinerad vitkål", 115),
                Item("Pulled beef", "med bulgur & bönor & marinerad vitkål", 115),
                Item("Pulled beef", "med potatis & marinerad vitkål", 115),
                Item("Pulled beef", "med pasta & marinerad vitkål", 115),
                Item("Pulled beef", "med blandade grönsaker & marinerad vitkål", 115),
                Item("Lax", "med pasta & thaisås", 110),
                Item("Lax", "med råris & senap/yoghurt", 110),
                Item("Lax", "med bulgur & bönor & ört/vitlökssås", 110),
                Item("Lax", "med potatis & ratatouille", 110),
                Item("Lax", "med bulgur & mangochili/yoghurt", 110),
                Item("Chorizo", "med potatis & marinerad vitkål & senapsås", 99),
                Item("Sanna's special", "Kycklingfilé, pasta, bönor, thaigryta, senapsås, cashew", 110),
                Item("Ako's fitnesstallrik", "Kycklingfilé, lax, quinoa, råris, ½ avokado, senapsås", 140),
                Item("LCHF", "Lax, quinoa, ägg, ½ avokado, senapsås", 130),
                Item("5:2", "bulgur, senapsås")]