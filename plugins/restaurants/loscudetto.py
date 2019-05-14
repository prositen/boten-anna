from plugins.restaurants.common import add_restaurant, Kvartersmenyn


@add_restaurant
class LoScudetto(Kvartersmenyn):
    url = 'http://www.kvartersmenyn.se/index.php/rest/15075'

    @staticmethod
    def name():
        return 'Lo Scudetto'

    @staticmethod
    def minutes():
        return 10