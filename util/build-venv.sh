#!/bin/bash
REQS="${1:?requirements}"
ZIP="${2:?zip file}"
DIR=/tmp/build$$
if ! test -e "$REQS"
then echo no reqs found ; exit 1
fi

mkdir -p "$DIR"
cp "$REQS" "$DIR"/requirements.txt
cd "$DIR"
virtualenv virtualenv
source virtualenv/bin/activate
pip install -r  requirements.txt
virtualenv/bin/python -m pip uninstall -y -q setuptools wheel pip
rm -f "$ZIP"
zip -r "$ZIP" virtualenv >/dev/null
ls -l $ZIP
rm -Rf "$DIR"

