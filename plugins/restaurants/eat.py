import datetime
from functools import lru_cache
import re
from bs4 import BeautifulSoup
import requests
from plugins.restaurants.common import Lunch, Item, add_restaurant

__author__ = 'anna'


@add_restaurant
class Eat(Lunch):
    url = "http://eatrestaurant.se/dagens/"
    week_header = re.compile(r'v\. (\d+) ')
    day_header = re.compile(r'(Mån|Tis|Ons|Tors|Fre):')

    @staticmethod
    def name():
        return "Eat"

    @staticmethod
    def minutes():
        return 5

    @lru_cache(32)
    def get(self, year, month, day):
        isocal = datetime.date(year, month, day).isocalendar()
        week = isocal[1]
        weekday = isocal[2]
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, "html.parser")
        entries = soup.find("div", {"class": "entry"}).find_all('p')
        found_week = False
        found_day = False
        menu_items = list()
        for entry in entries:
            text = entry.get_text().strip()
            week_result = self.week_header.match(text)
            if week_result:
                if found_week:
                    return menu_items
                if week == int(week_result.group(1)):
                    found_week = True
            else:
                if found_week:
                    day_result = self.day_header.match(text)
                    if day_result:
                        if found_day:
                            return menu_items
                        else:
                            this_day = day_result.group(1).lower()
                            if len(this_day) > 3:
                                this_day = this_day[0:3]
                            if weekday == self.DAYS[this_day]:
                                found_day = True

                    if found_day:
                        items = [Item(item.strip()) for item in text.split('\n') if not self.day_header.match(item)]
                        menu_items.extend(items)
        return menu_items
