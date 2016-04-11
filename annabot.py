from urllib.error import HTTPError
from slackbot.bot import Bot

__author__ = 'anna'


def main():
    try:
        bot = Bot()
        bot.run()
    except HTTPError as e:
        print(e.msg)

if __name__ == '__main__':
    main()
