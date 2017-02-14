from functools import lru_cache
from bs4 import BeautifulSoup
import re
import requests
from plugins.restaurants.common import Lunch, Item, add_restaurant, HeaderListParser

__author__ = 'anna'


@add_restaurant
class Wokhouse(Lunch, HeaderListParser):
    url = "http://www.wokhouse.net/lunch/"

    @staticmethod
    def name():
        return "Wokhouse"

    @staticmethod
    def minutes():
        return 8

    @lru_cache(32)
    def get(self, year, month, day):
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, "html.parser")
        day_re = re.compile('.* (\d+) \w+')

        headers = soup.find("div", {"id": "postcontent"}).findAll('h2')
        menu_items = []
        day_found = False
        for header in headers:
            day_result = day_re.match(header.get_text())
            if day_result is not None:
                if day == int(day_result.group(1)):
                    day_found = True
                else:
                    day_found = False
            else:
                day_found = True

            if day_found:
                items = header.next_sibling.next_sibling.find_all('strong')
                for item in items:
                    name = item.get_text()
                    desc = str(item.next_sibling).replace('-', '').replace('–','').strip()

                    menu_items.append(Item(name, desc=desc.strip(), cost=89))

                """
                items = str(header.next_sibling.next_sibling).replace('<br/>', '\n').split('\n')
                name_re = re.compile(r'<strong>(.*)</strong>')
                for i in items:

                    print('***')
                    print(i)

                    if '-' in i:
                        name, desc = i.split('-')
                    else:
                        name, desc = i.split('–')
                    name_res = name_re.search(name)
                    if name_res is not None:
                        name = name_res.group(1)

                    if desc.endswith('</p>'):
                        desc = desc[:-4]
                    print(name, desc)
                    menu_items.append(Item(name, desc=desc.strip(), cost=89))
                """
        return menu_items


