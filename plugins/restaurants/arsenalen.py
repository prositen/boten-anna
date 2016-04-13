from functools import lru_cache
from bs4 import BeautifulSoup
import requests
from plugins.restaurants.common import Lunch, Item, add_restaurant

__author__ = 'anna'


@add_restaurant
class Arsenalen(Lunch):
    url = "https://gastrogate.com/restaurang/arsenalen/page/3/"

    @staticmethod
    def name():
        return "Arsenalen"

    def parse_date(self, date):
        _, day, month = date.strip().split()
        return self.MONTHS[month[0:3]], int(day)

    @staticmethod
    def minutes():
        return 3

    @lru_cache(32)
    def get(self, year, month, day):
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, "html.parser")
        menu_table = soup.find('table', {'class': 'lunch_menu'})
        day_headers = menu_table.find_all('thead')
        for num, menu in enumerate(day_headers):
            menu_month, menu_day = self.parse_date(menu.find('th').get_text())
            if menu_month == month and menu_day == day:
                break
        else:
            return None
        menu = menu_table.find_all('tbody')[num]
        menu_items = menu.find_all('td', {'class': 'td_title'})
        items = []
        for item in menu_items:
            name = item.get_text().strip()
            cost_elem = item.parent.find('td', {'class': 'td_price'})
            cost = int(cost_elem.get_text().split(':')[0])
            items.append(Item(name, cost=cost))
        return items


