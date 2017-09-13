#!/bin/bash
PACKAGES="build-essential cmake pkg-config libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk2.0-dev libatlas-base-dev gfortran python2.7-dev python3-dev"
for PACKAGE in $PACKAGES
do
apt install -y $PACKAGE
done

#wget -O opencv.zip https://github.com/opencv/opencv/archive/3.3.0.zip
unzip opencv.zip

#wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.3.0.zip
unzip opencv_contrib.zip
