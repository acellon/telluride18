#!/bin/sh

echo "Installing dependencies and libraries..."
apt-get install bluetooth libbluetooth3 libboost-python-dev libboost-thread-dev libbluetooth-dev libglib2.0-dev python-dev python-bluez
pip install pybluez

echo "Adding pi to bluetooth group..."
in_group=`cat /etc/group | grep bluetooth | grep -o pi`
if [ $in_group ]; then
    usermod -G bluetooth -a pi
fi

echo "Changing /var/run/sdp group..."
chgrp bluetooth /var/run/sdp

echo "[Unit]
Descrption=Monitor /var/run/sdp

[Install]
WantedBy=bluetooth.service

[Path]
PathExists=/var/run/sdp
Unit=var-run-sdp.service
3.2. And another file, /etc/systemd/system/var-run-sdp.service:

[Unit]
Description=Set permission of /var/run/sdp

[Install]
RequiredBy=var-run-sdp.path

[Service]
Type=simple
ExecStart=/bin/chgrp bluetooth /var/run/sdp
" > /etc/systemd/system/var-run-sdp.path

echo "Editing dbus bluez service..."
sed -i '/^ExecStart=/usr/lib/bluetooth/bluetoothd/s/$/ --compat/' /etc/systemd/system/dbus-org.bluez.service

echo "Changing sdp permissions..."
chmod 777 /var/run/sdp

echo "Starting it all up..."
systemctl daemon-reload
systemctl enable var-run-sdp.path
systemctl enable var-run-sdp.service
systemctl start var-run-sdp.path
systemctl restart bluetooth
