#!/bin/sh

cd ~/pypboy

wget -q --spider http://google.com

if [ $? -eq 0 ]; then
    echo "Online"
    git pull
else
    echo "Offline"
fi

venv/bin/python -m cProfile -o ~/pypboy_profiles/`date +'%Y%m%d%H%M%S'` main.py
