# -*- coding: utf-8 -*-
from functools import lru_cache
import re
from bs4 import Tag, BeautifulSoup
import requests

__author__ = 'anna'


RESTAURANTS = []


def add_restaurant(cls):
    RESTAURANTS.append(cls())
    return cls


class Item(object):
    def __init__(self, name, desc=None, cost=None):
        self.name = name
        self.desc = desc
        if cost is None:
            self.cost = 0
        else:
            self.cost = cost

        if self.desc is not None:
            self.desc = self.desc.strip()
            if len(self.desc) == 0:
                self.desc = None

    def __str__(self):
        s = [self.name]
        if self.cost > 0:
            s.append(" ({0} kr)".format(self.cost))
        if self.desc is not None:
            s.append(": _{0}_".format(self.desc))
        return "".join(s)

    def search(self, query):
        if re.search(query, self.name, re.IGNORECASE):
            return True
        if self.desc is not None and re.search(query, self.desc, re.IGNORECASE):
            return True
        return False

    def match_cost(self, max_cost):
        return 0 < self.cost <= max_cost


class Lunch(object):
    url = ""

    @staticmethod
    def name():
        return "Lunch"

    @staticmethod
    def minutes():
        """ Minutes to walk from the office, according to Google Maps """
        return 0

    @lru_cache(32)
    def get(self, year, month, day):
        return []

    @staticmethod
    def nickname():
        return []

    def matches(self, where):
        if where is None:
            return True
        if self.name().lower() in where:
            return True
        if any([nick.lower() in where for nick in self.nickname()]):
            return True
        return False

    MONTHS = {'jan': 1,
              'feb': 2,
              'mar': 3,
              'apr': 4,
              'maj': 5,
              'may': 5,
              'jun': 6,
              'jul': 7,
              'aug': 8,
              'sep': 9,
              'oct': 10,
              'okt': 10,
              'nov': 11,
              'dec': 12
              }

    DAYS = {'mån': 1,
            'tis': 2,
            'ons': 3,
            'tor': 4,
            'fre': 5,
            'lör': 6,
            'sön': 7,
            'mon': 1,
            'tue': 2,
            'wed': 3,
            'thu': 4,
            'fri': 5,
            'sat': 6,
            'sun': 7
            }


class NoDaily(Lunch):
    def get(self, year, month, day):
        return [Item("No daily menu available", self.url)]


class HeaderListParser(object):
    """
    Parses documents on the form
    <A class="a">subsection</A>
    <B class="b">
        <C class="c">Food item</C>
        <D class="d">Food description</D>
        <E class="e">Food cost</D>
        ...
    </B>
    ...
    <A>...
    """
    url = ""

    def parse_page(self, soup=None,
                   header_elem="h3", header_elem_class=None, header_elem_id=None,
                   exclude_headers=None,
                   food_wrapper=None, food_wrapper_class=None,
                   name_elem=None, name_class=None,
                   desc_elem=None, desc_class=None,
                   cost_elem=None, cost_class=None):

        header_attribs = dict()
        if header_elem_id:
            header_attribs['id'] = header_elem_id
        if header_elem_class:
            header_attribs['class'] = header_elem_class
        headers = soup.find_all(header_elem, header_attribs)
        menu_items = []
        exclude_headers = [header.lower() for header in exclude_headers] if exclude_headers else []
        for header in headers:
            if header.get_text().strip().lower() not in exclude_headers:
                current = header.nextSibling
                while current is not None and current.name != header_elem:
                    if isinstance(current, Tag):
                        items = current.find_all(food_wrapper,
                                                 {"class": food_wrapper_class} if food_wrapper_class is not None else {})
                        if items is not None:
                            for item in items:
                                name = item.find(name_elem, {"class": name_class}).get_text().strip()
                                desc = item.find(desc_elem, {"class": desc_class})
                                cost = item.parent.find(cost_elem, {"class": cost_class})
                                if cost is not None:
                                    cost = int(cost.get_text().strip().split()[0], 10)
                                else:
                                    cost = 0
                                if desc is not None:
                                    desc = desc.get_text().strip()
                                    menu_items.append(Item(name, desc, cost))
                                else:
                                    menu_items.append(Item(name, cost=cost))
                    current = current.nextSibling
        return menu_items


class Foodora(Lunch, HeaderListParser):
    url = ""

    def parse_page(self, soup=None,
                   header_elem="h3", header_elem_class=None, header_elem_id=None,
                   exclude_headers=None,
                   food_wrapper=None, food_wrapper_class=None,
                   name_elem=None, name_class=None,
                   desc_elem=None, desc_class=None,
                   cost_elem=None, cost_class=None):
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, "html.parser")
        return super(Foodora, self).parse_page(soup,
                                               header_elem="div", header_elem_class="dish-category-header",
                                               exclude_headers=exclude_headers,
                                               food_wrapper="div", food_wrapper_class="dish-info",
                                               name_elem="h3", name_class="dish-name",
                                               desc_elem="p", desc_class="dish-description",
                                               cost_elem="span", cost_class="price"
                                               )


class Box(NoDaily):
    url = "http://saddesklunch.com/"

    @staticmethod
    def name():
        return "Box"

    @staticmethod
    def distance():
        return 0

    def get(self, year, month, day):
        return [Item(self.url)]

    @staticmethod
    def nickname():
        return ['Låda', 'Sad desk lunch']
