#!/usr/bin/python

from bot import Bot


def main():
    token = None
    with open("token", 'r') as f:
        token = f.readline()[:-1]
    bot = Bot(token)
    try:
        bot.start()
    except KeyboardInterrupt:
        bot.stop()
    bot.stop()

if __name__ == "__main__":
    main()
    