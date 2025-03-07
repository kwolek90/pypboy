#!/bin/sh

cd ~/pypboy

wget -q --spider http://google.com

if [ $? -eq 0 ]; then
    echo "Online"
    git pull
else
    echo "Offline"
fi

venv/bin/python main.py --ignore
