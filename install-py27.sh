#!/bin/sh
# Shell script to install dependencies on Terry's bootable Ubuntu USB

cd ~/git

pip install numpy
pip install scipy
pip install -e nengo
pip install -e nengo_gui

cd
