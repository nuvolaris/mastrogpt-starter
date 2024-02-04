#!/bin/bash
REQS="${1:?requirements}"
ZIP="${2:?zip file}"
DIR=/tmp/build$$
if ! test -e "$REQS"
then echo no reqs found ; exit 1
fi

mkdir -p "$DIR"
cp "$REQS" "$DIR"/package.json
cd "$DIR"
npm install 
rm -f "$ZIP"
zip -r "$ZIP" node_modules >/dev/null
ls -l $ZIP
rm -Rf "$DIR"

