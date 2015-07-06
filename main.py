#!/usr/bin/python

from server import Server
from bot import Bot
import os
import os.path

def parse():
    import argparse

    parser = argparse.ArgumentParser(description='Starts a bot')
    parser.add_argument("--purge", help="purges stuff", action="store_true")
    parser.add_argument("--webhook", help="uses webhook", type=str)
    parser.add_argument("--install", help="install with tocken", type=str, metavar='TOCKEN')
    args = parser.parse_args()
    return args.purge, args.webhook, args.install
    

def main():
    DIR = os.path.join(os.path.dirname(__file__), "botTest")
    TOCKEN_PATH = os.path.join(DIR, "token")
    UPDATES_LOG_PATH = os.path.join(DIR, "updates_log")
    purge, useWebhook, install = parse()
    if install != None:
        if not os.path.exists(DIR):
            os.mkdir(DIR)
        if not os.path.exists(UPDATES_LOG_PATH):
            with open(UPDATES_LOG_PATH, 'w') as f:
                f.write("")
        with open(TOCKEN_PATH, 'w') as f:
            f.write(install+"\n")
        print("End installing")
        return

    token = None
    with open(TOCKEN_PATH, 'r') as f:
        token = f.readline()[:-1]
    bot = Bot(token, "botTest")
    if purge:
        bot.setWebhook("")
        bot.start(purge)
        bot.getUpdates(purge)
        bot.stop()
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
    