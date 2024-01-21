#!/bin/bash
cd /mnt
virtualenv virtualenv
source virtualenv/bin/activate
pip install -r requirements.txt
yes | pip  uninstall setuptools wheel pip
zip -r virtualenv.zip virtualenv
rm -Rvf virtualenv
