#!/bin/sh

sudo apt-get update
sudo apt-get -y install python3 python3-pip python3-pygame vim python3-numpy python3-pil onboard

mkdir -p ~/.config/lxsession/LXDE-pi
cp /etc/xdg/lxsession/LXDE-pi/autostart ~/.config/lxsession/LXDE-pi
echo "@bash `pwd`/launcher.sh" >> ~/.config/lxsession/LXDE-pi/autostart
PANEL_SETTINGS=~/.config/lxpanel/LXDE-pi/panels/panel
cp /etc/xdg/lxpanel/LXDE-pi/panels/panel $PANEL_SETTINGS
ENABLE_NOTIFICATIONS="notifications=1"
DISABLE_NOTIFICATIONS="notifications=0"

# disable notifications
sudo sed -i -e "s/$ENABLE_NOTIFICATIONS/$DISABLE_NOTIFICATIONS/g" $PANEL_SETTINGS

python3 -m venv venv
venv/bin/python3 -m pip install -r requirements.txt