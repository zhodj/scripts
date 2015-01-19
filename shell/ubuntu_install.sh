#!/bin/bash
# ubuntu 14.04 tested
# authored by zhodj 1/19/2015

#base
sudo apt-get install build-essential -y
sudo apt-get install gcc-4.7 gcc-4.7-multilib g++-4.7 g++-4.7-multilib -y
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 50
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.7 40
sudo update-alternatives --config gcc
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.8 50
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.7 40
sudo update-alternatives --config g++

#java
sudo apt-get install python-software-properties -y
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java7-installer -y

#caffe
sudo apt-get install libatlas-base-dev -y
sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libboost-all-dev libhdf5-serial-dev -y
sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev protobuf-compiler -y
#cuda

