#!/bin/bash

DATADIR=$1
cd `dirname $0`

function wait_for_change {
  inotifywait -r \
    -e modify,move,create,delete \
    $DATADIR/json
}

while wait_for_change; do
  sleep 2
  rsync -rlt --delete $DATADIR/json www/data/
  /usr/bin/python ./bsq_json.py &
done

