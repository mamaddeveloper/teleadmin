#!/bin/bash

openssl req -newkey rsa:2048 -sha256 -nodes -keyout botTest/private.key -x509 -days 3650 -out botTest/public.pem -subj "/C=CH/ST=CH/L=CH/O=TelegramBot/CN=MyTelegramBot"
chmod 400 botTest/private.key
chmod 400 botTest/public.pem
