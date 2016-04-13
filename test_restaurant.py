from plugins.lunch import lunch_menu_command, lunch_search_command

__author__ = 'anna'

# from plugins.restaurants.eat import Eat


class MessageMock(object):

    def send(self, message):
        print(message)

    def send_webapi(self, text, attachment=""):
        print(text, attachment)


def main():
    lunch_menu_command(MessageMock(), 'wiggos')
    # lunch_search_command(MessageMock, 'max_cost=100')
    pass

if __name__ == '__main__':
    main()