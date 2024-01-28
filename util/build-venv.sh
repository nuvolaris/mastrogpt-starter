#!/bin/bash
REQS="${1:?requirements}"
ZIP="${2:?zip file}"
DIR=/tmp/build$$

mkdir -p "$DIR"
cp "$REQS" "$DIR"/requirements.txt
cd "$DIR"
virtualenv virtualenv
source virtualenv/bin/activate
pip install -r requirements.txt
yes | pip  uninstall setuptools wheel pip >/dev/null
zip -r "$ZIP" virtualenv >/dev/null
ls -l $ZIP
rm -Rf "$DIR"

