import datetime
import json
import random
from functools import lru_cache
import re
import requests
from bs4 import BeautifulSoup, Tag
from slackbot.bot import listen_to


class Lunch(object):
    @staticmethod
    def name():
        pass

    @lru_cache(32)
    def get(self, year, month, day):
        pass

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
        return ["No daily menu available, see " + self.url]


class Arsenalen(Lunch):

    url = "https://gastrogate.com/restaurang/arsenalen/page/3/"

    @staticmethod
    def name():
        return "Arsenalen"

    def parse_date(self, date):
        _, day, month = date.strip().split()
        return self.MONTHS[month[0:3]], int(day)

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
        return [item.get_text().strip() for item in menu_items]


class Subway(Lunch):

    url = "http://www.subway.se"

    SUBS = ['American Steakhouse Melt',
            'Subway Melt',
            'Spicy Italian',
            'Rostbiff',
            'Tonfisk',
            'Subway Club',
            'Italian B.M.T.']

    @staticmethod
    def name():
        return "Subway"

    def get(self, year, month, day):
        date = datetime.datetime(year, month, day)
        return ["Sub of the day: " + self.SUBS[date.isoweekday()]]


class Eat(Lunch):

    url = "http://eatrestaurant.se/dagens/"
    week_header = re.compile(r'v\. (\d+) ')
    day_header = re.compile(r'(Mån|Tis|Ons|Tors|Fre):')

    @staticmethod
    def name():
        return "Eat"

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
                            if weekday == self.DAYS[day_result.group(1).lower()[0:3]]:
                                found_day = True
                    else:
                        if found_day:
                            items = [item.strip() for item in text.split('\n')]
                            menu_items.extend(items)

        return menu_items


class Wiggos(Lunch):
    url = "http://wiggowraps.se/menus/huvudmeny/"

    @staticmethod
    def name():
        return "Wiggos"

    @lru_cache(32)
    def get(self, year, month, day):
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, "html.parser")
        h2s = soup.find("div", {"class": "entry-content"}).find_all("h2")
        menu_items = []
        for h2 in h2s:
            if h2.get_text().strip() not in ["Snacks", "Dryck"]:
                current = h2.nextSibling
                while current.name != 'h2':
                    if isinstance(current, Tag):
                        items = current.find_all("span", {"class": "foodmenudesc"})
                        if items is not None:
                            menu_items.extend([item.get_text().strip() for item in items])
                    current = current.nextSibling
        return menu_items


class Foodora(Lunch):
    url = ""

    def parse_page(self, excluded_headers):
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, "html.parser")
        h3s = soup.find_all("h3", {"class": "menu__items__title"})
        menu_items = []
        for h3 in h3s:
            if h3.get_text().strip() not in excluded_headers:
                current = h3.nextSibling
                while current is not None and current.name != 'h3':
                    if isinstance(current, Tag):
                        items = current.find_all("div", {"class": "menu__item__name"})
                        if items is not None:
                            menu_items.extend([item.get_text().strip() for item in items])
                    current = current.nextSibling
        return menu_items


class Panini(Foodora):
    url = "https://www.foodora.se/restaurant/hk5l/panini-hamngatan-15"

    @staticmethod
    def name():
        return "Panini"

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(["Mindre måltider", "Dryck"])


class SenStreetKitchen(Foodora):
    url = "https://www.foodora.se/restaurant/s6lx/sen-street-kitchen"

    @staticmethod
    def name():
        return "Sen Street Kitchen"

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(["Smårätter", "Dryck"])


RESTAURANTS = [Arsenalen(), Subway(), Eat(), Panini(), Wiggos(), SenStreetKitchen()]


def lunches(year, month, day, where=None):
    payload = dict()
    if where is not None:
        where = [w.strip().lower() for w in where.split(',')]
    for restaurant in RESTAURANTS:
        if where is None or restaurant.name().lower() in where:
            menu = restaurant.get(year, month, day)
            if menu is not None:
                payload[restaurant.name()] = {'menu': menu, 'url': restaurant.url}
    return payload


def restaurants():
    return '\n'.join([" • " + restaurant.name() for restaurant in sorted(RESTAURANTS, key=lambda k: k.name())])


def fallback(restaurant, items):
    return "*{0}*\n {1}".format(restaurant, bulletize(items))


def bulletize(items, bullet='•'):
    newline = "\n {0} ".format(bullet)
    return "{0} {1}".format(bullet, newline.join(items))


@listen_to("^!lunch$")
def lunch_command(message):
    help = ["!lunch list - shows all restaurants",
            "!lunch suggest - pick a random restaurant",
            "!lunch menu <restaurant> - show menu for the selected restaurant(s)"]
    message.send("\n".join(help))


@listen_to("^!lunch suggest$")
@listen_to("^!lunch suggest (\d+)")
def lunch_suggest_command(message, num=1):
    num = min(int(num), len(RESTAURANTS))
    names = ",".join([r.name() for r in random.sample(RESTAURANTS, int(num))])
    lunch_menu_command(message, names)


@listen_to("^!lunch list")
def lunch_list_command(message):
    message.send(restaurants())


@listen_to("^!lunch menu (.*)")
def lunch_menu_command(message, restaurant):
    today = datetime.datetime.today()
    try:
        menus = lunches(today.year, today.month, today.day, restaurant)
        for r, menu in menus.items():
            if len(menu['menu']) < 6:
                message.send(fallback(r, menu['menu']))
            else:
                attachments = [{
                    'pretext': "*{0}*".format(r),
                    'fallback': fallback(r, menu['menu'][0:3]),
                    'text': bulletize(menu['menu']),
                    'color': 'good',
                    'mrkdwn_in': ['pretext', 'text']
                }]
                message.send_webapi('', json.dumps(attachments))
    except:
        message.send("Something went wrong when scraping the restaurant page.")
