#!/bin/bash

#wget https://github.com/TheBigRoomXXL/tinyfeed/releases/latest/download/tinyfeed_linux_arm64

#sudo mv tinyfeed_linux_arm64 tinyfeed
#sudo chmod +x tinyfeed

sudo cp -r ./update_feeds.service /etc/systemd/system/
sudo cp -r ./update_feeds.timer /etc/systemd/system/

sudo systemctl enable update_feeds.service
sudo systemctl enable update_feeds.timer
