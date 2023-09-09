#!/bin/sh

cd /home/karol/pypboy

wget -q --spider http://google.com

if [ $? -eq 0 ]; then
    echo "Online"
    git pull
else
    echo "Offline"
fi

/usr/bin/python main.py pi
