# TelegramBot


## Installing

Python version 3.

The python library [Requests](http://docs.python-requests.org/en/latest/user/install/#install) is required.  

For now, you'll have to run installer like this :

    python3 main.py --install [tocken]

## Adding a module

To create a new module, create a file "modules/mod_\<mod_name\>.py". 
A module is a class named Module\<ModuleName\> which inherits ModuleBase. Each ModuleBase's functions are called by the bot, in an event-like manner. You can override any of them to create you own bot.

## Removing a module

To remove a module, remove the file in the "modules/" folder. If you want to keep a module but don't want to load it, you can edit the "botTest/modules_exclude_local" text file.

