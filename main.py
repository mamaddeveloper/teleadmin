#!/usr/bin/python

from server import Server
from bot import Bot

def parse():
    import argparse

    parser = argparse.ArgumentParser(description='Starts a bot')
    parser.add_argument("--purge", help="purges stuff", action="store_true")
    parser.add_argument("--webhook", help="uses webhook", type=str)
    args = parser.parse_args()
    return args.purge, args.webhook
    

def main():
    purge, useWebhook = parse()
    token = None
    with open("botTest/token", 'r') as f:
        token = f.readline()[:-1]
    bot = Bot(token, "botTest")
    if purge:
        bot.setWebhook("")
        bot.getUpdates(purge)
        return
    if useWebhook:
        bot.setWebhook(useWebhook)
        server = Server()
        server.addBot(bot)
        server.run()
    else:
        bot.setWebhook("")
        try:
            bot.start(False)
        except KeyboardInterrupt:
            bot.stop()
            return
    

if __name__ == "__main__":
    main()
    