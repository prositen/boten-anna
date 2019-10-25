from plugins.lunch import lunch_menu_command, lunch_search_command, lunch_show_all

__author__ = 'anna'


# from plugins.restaurants.eat import Eat


class MessageMock(object):

    def send(self, text):
        print(text)

    def send_webapi(self, text, attachment=""):
        print(text, attachment)


def main():
    lunch_menu_command(MessageMock(), 'elverket')
    # lunch_show_all(MessageMock())
    # lunch_search_command(MessageMock(), 'chicken;max_cost=100')
    # lunch_menu_command(MessageMock(), 'eat')
    pass


if __name__ == '__main__':
    main()
