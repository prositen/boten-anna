import random
from slackbot.bot import listen_to
from plugins.helpers import *
from plugins.lunch_restaurants import *

RESTAURANTS = [Arsenalen(), Subway(), Eat(), Panini(), Wiggos(), SenStreetKitchen(),
               Vapiano(), IchaIcha(), Phils(), Fridays(), Prime()]


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
    return ", ".join([restaurant.name() for restaurant in sorted(RESTAURANTS, key=lambda k: k.name())])


@listen_to("^!lunch$")
def lunch_command(message):
    command_help = ["!lunch list - shows all restaurants",
                    "!lunch suggest - pick a random restaurant",
                    "!lunch menu <restaurant> - show menu for the selected restaurant(s)",
                    "!lunch search <query>;<<query> - text search in menu, + special operator max_dist=X"]
    message.send("\n".join(command_help))


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
                message.send_webapi('', format_menu(r, menu['menu']))
    except Exception as e:
        message.send("Something went wrong when scraping the restaurant page.")
        print(e)


LUNCH_SEARCH_DIST = re.compile(r'max_dist=(\d+)')


@listen_to("^!lunch search (.*)")
def lunch_search_command(message, query_string):
    today = datetime.datetime.today()
    menus = lunches(today.year, today.month, today.day)
    queries = query_string.split(";")
    rs = RESTAURANTS
    show_items = False

    for query in queries:
        query = query.strip()
        result = LUNCH_SEARCH_DIST.match(query)
        if result:
            dist = int(result.group(1))
            rs = [r for r in rs if r.minutes() <= dist]
            continue

        show_items = True
        new_menus = dict()
        for r in rs:
            name = r.name()
            menu = [item for item in menus[name]['menu'] if re.search(query, item, re.IGNORECASE)]
            if len(menu):
                new_menus[name] = menu
        menus = new_menus
        rs = [r for r in rs if r.name() in menus.keys()]
    if show_items:
        for r in rs:
            message.send_webapi('', format_menu(r.name(), menus[r.name()]))
    else:
        message.send(bulletize([r.name() for r in rs]))

