# Making Bluetooth (and PyBluez) work on Raspberry Pi Zero W

_N.B. You can skip directly to step 8 by using the bash script `bdfix.sh`._

1.  Install necessary dependencies and libraries:

        $ sudo apt-get install bluetooth libbluetooth3 libboost-python-dev libboost-thread-dev libbluetooth-dev libglib2.0-dev python-dev python-bluez
        $ sudo pip install pybluez


2.  Check if your pi is in the bluetooth group:

        $ cat /etc/group | grep bluetooth
        bluetooth:x:113:pi

    *   If pi is not in group, add:

            $ sudo usermod -G bluetooth -a pi   

3.  Change group of the /var/run/sdp file:

        $ sudo chgrp bluetooth /var/run/sdp


4.  Make the change persistent after reboot by creating file `/etc/systemd/system/var-run-sdp.path` with the following  content:

        [Unit]
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


5.  Next, edit the file `/etc/systemd/system/dbus-org.bluez.service` by changing the line

        ExecStart=/usr/lib/bluetooth/bluetoothd

    to

        ExecStart=/usr/lib/bluetooth/bluetoothd --compat

6.  Change the permissions on   `/var/run/sdp` with the command

        $ sudo chmod 777 /var/run/sdp

7.  Finally, start it all up:

        $ sudo systemctl daemon-reload
        $ sudo systemctl enable var-run-sdp.path
        $ sudo systemctl enable var-run-sdp.service
        $ sudo systemctl start var-run-sdp.path
        $ sudo systemctl restart bluetooth

8.  After starting up, you may need to reboot the system. Then, to make the pi discoverable, use the command:

        $ sudo hciconfig hci0 piscan

9.  The pi's bluetooth address can be found by using the command `hciconfig`.
10. Minimal example client/server files are available.
