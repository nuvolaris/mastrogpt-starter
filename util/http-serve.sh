#!/bin/bash
if test -e /tmp/nuv-poll.pid
then
    PID=$(cat /tmp/nuv-poll.pid 2>/dev/null)
    if test -e /proc/$PID
    then kill -9 $PID 
    fi
fi
nuv -wsk activation poll & echo $! >/tmp/nuv-poll.pid

if test -e /tmp/http-serve.pid
then
    PID=$(cat /tmp/http-serve.pid 2>/dev/null)
    if test -e /proc/$PID
    then kill -9 $PID
    fi
fi
echo $$ >/tmp/http-serve.pid
exec http-server -a 127.0.0.1 web -c-1 --mimetypes util/mime.types -P $NUVDEV_HOST
