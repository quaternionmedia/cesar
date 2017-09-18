#!/bin/bash
PACKAGES="build-essential cmake pkg-config libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk2.0-dev libatlas-base-dev gfortran python2.7-dev python3-dev"
for PACKAGE in $PACKAGES
do
apt install -y $PACKAGE
done

wget -O opencv-3.3.0.zip https://github.com/opencv/opencv/archive/3.3.0.zip
unzip opencv-3.3.0.zip

wget -O opencv_contrib-3.3.0.zip https://github.com/opencv/opencv_contrib/archive/3.3.0.zip
unzip opencv_contrib-3.3.0.zip

#pip install numpy

cd opencv-3.3.0
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
		-D CMAKE_INSTALL_PREFIX=/usr/local \
		-D INSTALL_PYTHON_EXAMPLES=OFF \
		-D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.3.0/modules \
		-D INSTALL_C_EXAMPLES=OFF \
		-D BUILD_EXAMPLES=OFF \
		-D PYTHON3_EXECUTABLE=/usr/local/bin/python3.6 \
		-D PYTHON3_INCLUDE=/usr/local/include/python3.6m \
		-D PYTHON3_LIBRARY=/usr/local/lib/libpython3.6m.a \
		-D PYTHON3_PACKAGES_PATH=/usr/local/lib/python3.6/site-packages \
		-D PYTHON3_NUMPY_INCLUDE_DIRS=/usr/local/lib/python3.6/dist-packages/numpy/core/include ..
