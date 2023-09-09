#!/bin/sh

sudo apt-get update
sudo apt-get install python3 python3-pip python3-pygame vim git python3-numpy python3-pil
git clone https://github.com/goodtft/LCD-show.git
git clone https://github.com/kwolek90/pypboy.git
pip install xmltodict requests
mkdir -p ~/.config/lxsession/LXDE-pi
cp /etc/xdg/lxsession/LXDE-pi/autostart ~/.config/lxsession/LXDE-pi
echo "@python3 `pwd`/pypboy/main.py pi" >> ~/.config/lxsession/LXDE-pi/autostart
cd LCD-show
sudo chmod +x LCD35-show
sudo ./LCD35-show