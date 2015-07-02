# TelegramBot


## Installing

Python version 3.

The python library [Requests](http://docs.python-requests.org/en/latest/user/install/#install) is required.  

For now, you'll have to create a file named "botTest/token" which contains you bot's token.
A file named "botTest/updates_log" must be created too.

## Adding a module

To create a new module, create a file "modules/mod_\<mod_name\>.py". 
A module is a class named Module\<ModuleName\> which inherits ModuleBase. Each ModuleBase's functions are called by the bot, in an event-like manner. You can override any of them to create you own bot.

## Removing a module

To remove a module, remove the file in the "modules/" folder. If you want to keep a module but don't want to load it, you can edit the excluded_modules text file.

