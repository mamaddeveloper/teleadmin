#!/usr/bin/python3

from server import *
from bot import Bot
import json
import logging
import logging.config
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
    LOGGING_PATH = os.path.join(os.path.join(os.path.dirname(__file__), "logs"), "config.json")
    PRIVATE_KEY_PATH = os.path.join(os.path.dirname(__file__), "botTest/private.key")
    PUBLIC_KEY_PATH = os.path.join(os.path.dirname(__file__), "botTest/public.pem")
    purge, useWebhook, install = parse()
    if install != None:
        if not os.path.exists(DIR):
            os.mkdir(DIR)
        with open(TOCKEN_PATH, 'w') as f:
            f.write(install+"\n")
        print("End installing")
        return

    if os.path.exists(LOGGING_PATH):
        with open(LOGGING_PATH, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.DEBUG)

    token = None
    with open(TOCKEN_PATH, 'r') as f:
        token = f.readline()[:-1]
    bot = Bot(token, DIR)
    if purge:
        bot.purge()
        return
    server = None
    if useWebhook:
        if not os.path.exists(PUBLIC_KEY_PATH):
            print("No public key, please run ssl.sh before !")
            return
        if not os.path.exists(PRIVATE_KEY_PATH):
            print("No private key, please run ssl.sh before !")
            return
        server = Server(bot, PUBLIC_KEY_PATH, PRIVATE_KEY_PATH)
    else:
        server = PollingServer(bot)
    print("### Start bot...")
    bot.start()
    print("### Bot started")
    print("### Start server...")
    server.start()
    print("### Server started")
    try:
        while True:
            time.sleep(60*60)
    except KeyboardInterrupt:
        pass
    print("### Stop server...")
    server.stop()
    print("### Server stopped")
    print("### Stop bot...")
    bot.stop()
    print("### Bot stopped")
    print("### Join server...")
    server.join()
    print("### Server joined")
    print("### Join bot...")
    bot.join()
    print("### Bot joined")
    print("### End of main")

if __name__ == "__main__":
    main()
