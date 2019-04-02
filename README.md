Tio Chema
=========

tio_chema is a simple IRC bot, made with love by and for the [Guatemalan Free Software Community](http://slgt.org). Features an extendable design, non-blocking, concurrent plugins, where the base API is simple and each plugins implement it's own functionality, without making things complicated.

PLZ HELP: see [our TODO list!](TODO.md)

Installation
-----------

Library depends
* python-twisted
* python-yapsy
* python-twython

    bash devel_setup.sh

Usage
-----

### Activate the virtual enviroment (optional)

    source venv/bin/activate

### Install the dependencies

    pip install -r requirements.txt

### Edit the bot.cf file to your convenience


### Run bot_chema.py

    python bot_chema.py bot.cf

Testing
-------

Pending

Plugin Architecture
-------------------

Plugins are based in YAPSY plugins, you can inherit from BasePlugin and TextTriggerPlugin (a generic trigger behaviour)
