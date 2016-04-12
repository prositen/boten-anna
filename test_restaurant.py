from plugins.lunch import lunch_menu_command

__author__ = 'anna'

# from plugins.restaurants.eat import Eat


class MessageMock(object):

    def send(self, message):
        print(message)

    def send_webapi(self, derp, message):
        print(message)


def main():
    lunch_menu_command(MessageMock(), 'eat')
    pass

if __name__ == '__main__':
    main()