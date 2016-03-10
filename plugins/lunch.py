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


class HeaderListParser(object):
    """
    Parses documents on the form
    <A class="a">subsection</A>
    <B class="b">
        <C class="c">Food item</C>
        <D class="d">Food description</D>
        ...
    </B>
    ...
    <A>...
    """
    url = ""

    def parse_page(self, soup=None,
                   header_elem="h3", header_elem_class=None,
                   exclude_headers=None,
                   food_wrapper=None, food_wrapper_class=None,
                   name_elem=None, name_class=None,
                   desc_elem=None, desc_class=None):

        headers = soup.find_all(header_elem, {"class": header_elem_class} if header_elem_class is not None else {})
        menu_items = []
        for header in headers:
            if header.get_text().strip() not in exclude_headers:
                current = header.nextSibling
                while current is not None and current.name != header_elem:
                    if isinstance(current, Tag):
                        items = current.find_all(food_wrapper,
                                                 {"class": food_wrapper_class} if food_wrapper_class is not None else {})
                        if items is not None:
                            for item in items:
                                name = item.find(name_elem, {"class": name_class}).get_text().strip()
                                desc = item.find(desc_elem, {"class": desc_class})
                                if desc is not None:
                                    desc = desc.get_text().strip()
                                    menu_items.append("{0}: _{1}_".format(name, desc))
                                else:
                                    menu_items.append(name)
                    current = current.nextSibling
        return menu_items


class Wiggos(Lunch, HeaderListParser):
    url = "http://wiggowraps.se/menus/huvudmeny/"

    @staticmethod
    def name():
        return "Wiggos"

    def parse_page(self, soup=None,
                   header_elem="h3", header_elem_class="None",
                   exclude_headers=None,
                   food_wrapper=None, food_wrapper_class=None,
                   name_elem=None, name_class=None,
                   desc_elem=None, desc_class=None):

        return super(Wiggos, self).parse_page(soup,
                                              header_elem="h2", exclude_headers=["Snacks", "Dryck"],
                                              food_wrapper="span", food_wrapper_class="foodmenuwrap",
                                              name_elem="span", name_class="foodmenudesc",
                                              desc_elem="span", desc_class="fooddesc")

    @lru_cache(32)
    def get(self, year, month, day):
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, "html.parser")
        content = soup.find("div", {"class": "entry-content"})
        return self.parse_page(content)


class Foodora(Lunch, HeaderListParser):
    url = ""

    def parse_page(self, soup=None,
                   header_elem="h3", header_elem_class=None,
                   exclude_headers=None,
                   food_wrapper=None, food_wrapper_class=None,
                   name_elem=None, name_class=None,
                   desc_elem=None, desc_class=None):

        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, "html.parser")
        return super(Foodora, self).parse_page(soup,
                                               header_elem="h3", header_elem_class="menu__items__title",
                                               exclude_headers=exclude_headers,
                                               food_wrapper="div", food_wrapper_class="menu__item__wrapper",
                                               name_elem="div", name_class="menu__item__name",
                                               desc_elem="div", desc_class="menu__item__description"
                                               )


class Panini(Foodora):
    url = "https://www.foodora.se/restaurant/hk5l/panini-hamngatan-15"

    @staticmethod
    def name():
        return "Panini"

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(exclude_headers=["Mindre måltider", "Dryck"])


class SenStreetKitchen(Foodora):
    url = "https://www.foodora.se/restaurant/s6lx/sen-street-kitchen"

    @staticmethod
    def name():
        return "Sen Street Kitchen"

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(exclude_headers=["Smårätter", "Dryck"])


class Vapiano(NoDaily):
    url = "http://se.vapiano.com/sv/meny/specials/"

    @staticmethod
    def name():
        return "Vapiano"

RESTAURANTS = [Arsenalen(), Subway(), Eat(), Panini(), Wiggos(), SenStreetKitchen(),
               Vapiano()]


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
