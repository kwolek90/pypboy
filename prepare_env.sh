#!/bin/sh

sudo apt-get update
sudo apt-get -y install python python-pip python-pygame vim git python-numpy python-pil onboard
git clone https://github.com/kwolek90/pypboy.git
pip install xmltodict requests
mkdir -p ~/.config/lxsession/LXDE-pi
cp /etc/xdg/lxsession/LXDE-pi/autostart ~/.config/lxsession/LXDE-pi
echo "@bash `pwd`/pypboy/launcher.sh" >> ~/.config/lxsession/LXDE-pi/autostart
PANEL_SETTINGS=~/.config/lxpanel/LXDE-pi/panels/panel
cp /etc/xdg/lxpanel/LXDE-pi/panels/panel $PANEL_SETTINGS
ENABLE_NOTIFICATIONS="notifications=1"
DISABLE_NOTIFICATIONS="notifications=0"

# disable notifications
sudo sed -i -e "s/$ENABLE_NOTIFICATIONS/$DISABLE_NOTIFICATIONS/g" $PANEL_SETTINGS

cp `pwd`/pypboy/launcher.sh run
cd ~/pypboy
venv/bin/python -m pip install -r requirements.txt