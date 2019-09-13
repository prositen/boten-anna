import datetime
import random
from slackbot.bot import listen_to, respond_to
import re
from plugins.helpers import *
from plugins.restaurants.common import RESTAURANTS
from plugins.restaurants import *


class SearchResult(object):
    def __init__(self, name, menu, url, distance):
        self.name = name
        self.menu = menu
        self.url = url
        self.distance = distance

    def menu_as_string(self):
        return ",".join([str(s) for s in self.menu])


def lunches(year, month, day, where=None):
    payload = dict()
    if where is not None:
        where = [w.strip().lower() for w in where.split(',')]
    for restaurant in RESTAURANTS:
        if restaurant.matches(where):
            try:
                menu = restaurant.get(year, month, day)
                if menu is not None:
                    payload[restaurant.name()] = SearchResult(restaurant.name(), menu,
                                                              restaurant.url, restaurant.minutes())
            except Exception as e:
                print(str(e))

    return payload


def restaurant_list():
    return ", ".join([restaurant.name()
                      for restaurant in sorted(RESTAURANTS,
                                               key=lambda k: k.name())])


@listen_to("^!lunch$")
@listen_to("^!lunch help$")
@respond_to("^!lunch$")
@respond_to("^!lunch help$")
def lunch_command(message):
    command_help = ["!lunch help - show this text",
                    "!lunch list - shows all restaurants",
                    "!lunch suggest - pick a random restaurant",
                    "!lunch menu <restaurant> - show menu for the selected restaurant(s)",
                    "!lunch search <query>;<<query> - text search in menu, "
                    "+ special operator max_dist=X"]
    message.send_webapi("\n".join(command_help))


@listen_to(r"^!lunch suggest$")
@listen_to(r"^!lunch suggest (\d+)")
@respond_to(r"^!lunch suggest$")
@respond_to(r"^!lunch suggest (\d+)")
def lunch_suggest_command(message, num=1):
    num = min(int(num), len(RESTAURANTS))
    names = ",".join([r.name() for r in random.sample(RESTAURANTS, int(num))])
    lunch_menu_command(message, names)


@listen_to("^!lunch list")
@respond_to("^!lunch list")
def lunch_list_command(message):
    message.send_webapi(restaurant_list())


@listen_to(r"^!lunch menu (.*)")
@respond_to(r"^!lunch menu (.*)")
def lunch_menu_command(message, restaurant):
    today = datetime.datetime.today()
    try:
        search_results = lunches(today.year, today.month, today.day, restaurant)
        for s in search_results.values():
            if len(s.menu) == 0:
                message.send_webapi(fallback(s.name, ['No menu found today']))
            elif len(s.menu) < 6:
                message.send_webapi(fallback("{} ({} min)". format(s.name, s.distance), s.menu))
            else:
                message.send_webapi('', format_menu(s.name, s.distance, s.menu))
    except Exception as e:
        message.send_webapi("Something went wrong when scraping the restaurant page.")
        print(e)


LUNCH_SEARCH_DIST = re.compile(r'max_dist=(\d+)')
LUNCH_SEARCH_COST = re.compile(r'max_cost=(\d+)')


def filter_items(search_results, func):
    new_results = dict()
    for name, restaurant in search_results.items():
        menu = restaurant.menu
        menu_items = [item for item in menu if func(item)]
        if len(menu_items):
            new_results[name] = SearchResult(name, menu_items, restaurant.url, restaurant.distance)
    return new_results


@listen_to("^!lunch search (.*)")
@respond_to("^!lunch search (.*)")
def lunch_search_command(message, query_string):
    today = datetime.datetime.today()
    search_results = lunches(today.year, today.month, today.day)
    queries = query_string.split(";")
    show_items = False

    for query in queries:
        query = query.strip()
        result = LUNCH_SEARCH_DIST.match(query)
        if result:
            dist = int(result.group(1))
            search_results = filter_items(search_results, lambda x: x.distance <= dist)
            continue

        result = LUNCH_SEARCH_COST.match(query)
        if result:
            show_items = True
            max_cost = int(result.group(1))
            search_results = filter_items(search_results, lambda x: x.match_cost(max_cost))
            continue

        show_items = True
        search_results = filter_items(search_results, lambda x: x.search(query))

    if len(search_results) == 0:
        message.send_webapi("Found nothing")

    elif show_items:
        for s in search_results.values():
            message.send_webapi('', format_menu(s.name, s.distance, s.menu))

    else:
        return message.send_webapi(bulletize([s.name for s in search_results]))

