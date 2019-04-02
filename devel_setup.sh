#!/usr/bin/env bash

virtualenv --no-site-packages venv -p python2
source venv/bin/activate

pip install twisted yapsy configobj tweepy praw beautifulsoup4
pip install -r requirements.txt
