#!/usr/bin/python

from server import Server
from bot import Bot


def main():
    token = None
    with open("botTest/token", 'r') as f:
        token = f.readline()[:-1]
    bot = Bot(token, "botTest")
    server = Server()
    server.addBot(bot)
    server.run()
    

if __name__ == "__main__":
    main()
    