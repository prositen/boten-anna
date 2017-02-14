import datetime
from functools import lru_cache
import re
from bs4 import BeautifulSoup
import requests
from plugins.restaurants.common import Lunch, Item, add_restaurant

__author__ = 'anna'


@add_restaurant
class Tures(Lunch):
    url = "http://www.brasserietures.se/"

    @staticmethod
    def name():
        return "Tures"

    @staticmethod
    def minutes():
        return 11

    @lru_cache(32)
    def get(self, year, month, day):
        day_header = re.compile(r'(Mån|Tis|Ons|Tor|Fre)', re.IGNORECASE)
        isocal = datetime.date(year, month, day).isocalendar()
        weekday = isocal[2]
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, "html.parser")
        rows = soup.find("table", {"class": "mceItemTable"}).findAll('tr')
        found_day = False
        menu_items = []
        for row in rows:
            tds = row.findAll('td')
            td = tds[2]
            td_text = td.get_text().strip()
            day_result = day_header.match(td_text)
            if day_result:
                if found_day:
                    found_day = False
                elif weekday == self.DAYS[day_result.group(1).lower()]:
                    found_day = True
            else:
                if td_text.lower() == "klassiker":
                    found_day = True
                if found_day:
                    ps = td.findAll('p')
                    if len(ps):
                        name = ps[0].get_text().strip()
                        desc = ps[1].get_text().strip()
                        cost = tds[3].get_text().strip()
                        if len(cost):
                            cost = int(cost.split(':')[0])
                            menu_items.append(Item(name, desc, cost))
        return menu_items
