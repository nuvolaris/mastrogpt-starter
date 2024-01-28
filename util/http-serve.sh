#!/bin/bash
PID=$(cat /tmp/nuv-poll.pid)
if test -e /proc/$PID
then kill -9 $PID
fi
nuv -wsk activation poll & echo $! >/tmp/nuv-poll.pid

PID=$(cat /tmp/http-serve.pid)
if test -e /proc/$PID
then kill -9 $PID
fi
echo $$ >/tmp/http-serve.pid
exec http-server -a 127.0.0.1 web -c-1 --mimetypes util/mime.types -P $NUVDEV_HOST
