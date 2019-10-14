#!/usr/bin/bash

BasePath=$PWD
InstallPath="/opt/SmittenBooth"

sudo mkdir -p $InstallPath
sudo chown -R $USER:$USER $InstallPath
cp -r $BasePath/includes $BasePath/photobooth.py $InstallPath/
sed -i 's/{user}/'"$USER"'/g' $InstallPath/includes/systemd/photobooth.service
sudo cp $InstallPath/includes/systemd/photobooth.service /lib/systemd/system/photobooth.service
sudo systemctl enable photobooth.service

echo "To Start use command: sudo systemctl start photobooth.service"
