#!/usr/bin/env bash

curl -O https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
tar xzvf Python-3.6.1.tgz
ROOT=`pwd`

cd Python-3.6.1/
./configure --prefix=$ROOT/bin/Python3/
make && make install
$ROOT/bin/Python3/bin/pip3 install -r $ROOT/requirements.txt
cd $ROOT
rm Python-3.6.1.tgz
rm -r Python-3.6.1/




