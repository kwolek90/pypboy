#!/bin/sh

sudo apt-get update
sudo apt-get -y install python3 python3-pip python3-pygame vim git python3-numpy python3-pil onboard
git clone https://github.com/goodtft/LCD-show.git
git clone https://github.com/kwolek90/pypboy.git
pip install xmltodict requests pyky040
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
cd LCD-show
sudo chmod +x LCD35-show
sudo ./LCD35-show