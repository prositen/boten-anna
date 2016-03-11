import datetime
from functools import lru_cache
from bs4 import BeautifulSoup, Tag
import re
import requests

__author__ = 'anna'


class Item(object):
    def __init__(self, name, desc=None):
        self.name = name
        self.desc = desc

    def __str__(self):
        if self.desc is not None and len(self.desc.strip()):
            return "{0}: _{1}_".format(self.name, self.desc)
        else:
            return self.name


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
        return [Item(item.get_text().strip()) for item in menu_items]


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

    @staticmethod
    def minutes():
        return 7

    def get(self, year, month, day):
        date = datetime.datetime(year, month, day)
        return [Item("Sub of the day: " + self.SUBS[date.isoweekday()])]


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
                            if weekday == self.DAYS[day_result.group(1).lower()[0:3]]:
                                found_day = True
                    else:
                        if found_day:
                            items = [Item(item.strip()) for item in text.split('\n')]
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
        if exclude_headers:
            exclude_headers = [header.lower() for header in exclude_headers]
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
                                if desc is not None:
                                    desc = desc.get_text().strip()
                                    menu_items.append(Item(name, desc))
                                else:
                                    menu_items.append(Item(name))
                    current = current.nextSibling
        return menu_items


class Wiggos(Lunch, HeaderListParser):
    url = "http://wiggowraps.se/menus/huvudmeny/"

    @staticmethod
    def name():
        return "Wiggos"

    @staticmethod
    def minutes():
        return 5

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

    @staticmethod
    def minutes():
        return 1

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(exclude_headers=["Mindre måltider", "Dryck"])


class SenStreetKitchen(Foodora):
    url = "https://www.foodora.se/restaurant/s6lx/sen-street-kitchen"

    @staticmethod
    def name():
        return "Sen Street Kitchen"

    @staticmethod
    def minutes():
        return 5

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(exclude_headers=["Smårätter", "Dryck"])


class Vapiano(NoDaily):
    url = "http://se.vapiano.com/sv/meny/specials/"

    @staticmethod
    def name():
        return "Vapiano"

    @staticmethod
    def minutes():
        return 9


class IchaIcha(Lunch):
    url = "http://www.ichaicha.se/menu/"

    @staticmethod
    def name():
        return "IchaIcha"

    @staticmethod
    def minutes():
        return 3

    def get(self, year, month, day):
        return [Item("Nudlar", "Kokta äggnudlar med grönsaker"),
                Item("Japanskt ris", "Ångat mellankornigt ris och grönsaker"),
                Item("Lowcarb", " Strimlad zucchini (kyld) med babyspenat, broccoli och grönsaker."),
                Item("Kyckling", " Ungsstek strimlad lårfilé från Svensk gårdskyckling"),
                Item("Laxfilé", " Norsk superior-lax. Lätt saltad och tillagad i ugn"),
                Item("Fläsksida", " Från Rocklunda gård. Rimmad och tillagad på låg temp."),
                Item("Nötkött", " Rosastekt Highland beef, strip steak. Skottland."),
                Item("Teriyaki", " Söt, mild, soja. Fettfri."),
                Item("Ingefära", " Massor av ingefära!"),
                Item("Spicy sour", " Pressad citron, chili.")]


class Phils(Lunch):
    url = "http://www.philsburger.se/#pmeny"

    @staticmethod
    def name():
        return "Phils"

    @staticmethod
    def minutes():
        return 10

    @lru_cache(32)
    def get(self, year, month, day):
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, "html.parser")
        menu = soup.find("h4", {"class": "items-title"})
        menu_items = []
        n = menu.nextSibling
        while n is not None and n.name != 'div':
            n = n.nextSibling
        for item in n.findAll("div", {"class": "food"}):
            name_elem = item.find("h4", {"class": "title"})
            desc = name_elem.parent.nextSibling.strip()
            name = name_elem.next.strip()
            menu_items.append(Item(name, desc))
        return menu_items


class Fridays(Lunch):
    SPECIAL = ["Premium Burgers",
               "Ribs Ribs Ribs",
               "Steaks"]

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
        return [Item("Bacon Cheeseburger"), Item("Chicken Caesar Salad"), Item("Chicken Finger BLT Sandwich"),
                Item("Crispy Chicken Tenders"), Item("Lemon Basil Salad"), Item("Buffalo Chicken Sandwich"),
                Item("Jack Daniel's Burger"), Item("Romesco Grilled Vegetable Pasta"),
                Item("Jack Daniel's Chicken Burger"), Item("Fridays Finest Falafel"),
                Item("Tennessee BBQ Pulled Pork Sandwich"), Item("Creamy Buffalo Chicken Pasta"),
                Item("Weekly Special: {0}".format(self.SPECIAL[week]))]


class Prime(Foodora):
    url = "https://www.foodora.se/restaurant/s8ci/prime-burger-birger-jarlsgatan"

    @staticmethod
    def name():
        return "Prime"

    @staticmethod
    def minutes():
        return 15

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(exclude_headers=["Side Orders", "Milkshakes", "Soft Drinks"])


class Eggs(Foodora):
    url = "https://www.foodora.se/restaurant/s6bo/eggs-inc"

    @staticmethod
    def name():
        return "Eggs"

    @staticmethod
    def minutes():
        return 5

    @lru_cache(32)
    def get(self, year, month, day):
        return self.parse_page(exclude_headers=["Äggägg", "Dessert", "Dryck", "Extra", "Äggwrap"])