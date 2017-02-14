from plugins.restaurants.common import Lunch, Item, add_restaurant

__author__ = 'anna'


@add_restaurant
class IchaIcha(Lunch):
    url = "http://www.ichaicha.se/menu/"

    @staticmethod
    def name():
        return "IchaIcha"

    @staticmethod
    def minutes():
        return 10

    def get(self, year, month, day):
        return [Item("Nudlar", "Kokta äggnudlar med grönsaker"),
                Item("Japanskt ris", "Ångat mellankornigt ris och grönsaker"),
                Item("Lowcarb", "Strimlad zucchini (kyld) med babyspenat, broccoli och grönsaker."),
                Item("Kyckling", "Ungsstek strimlad lårfilé från Svensk gårdskyckling", 99),
                Item("Laxfilé", "Norsk superior-lax. Lätt saltad och tillagad i ugn", 109),
                Item("Fläsksida", "Från Rocklunda gård. Rimmad och tillagad på låg temp.", 109),
                Item("Nötkött", "Rosastekt Highland beef, strip steak. Skottland.", 129),
                Item("Teriyaki", "Söt, mild, soja. Fettfri."),
                Item("Ingefära", "Massor av ingefära!"),
                Item("Spicy sour", "Pressad citron, chili.")]

    @staticmethod
    def nickname():
        return ['Icha', 'Icha Icha']
