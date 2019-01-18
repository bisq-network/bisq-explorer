#!/bin/bash

DATADIR=/home/explorer/.local/share/seedNode/btc_testnet/db
EXPLORER_HOME=/home/explorer/explorer

while true
do
echo `date`  "(Re)-starting update_data.sh"
$EXPLORER_HOME/update_data.sh $DATADIR > /dev/null 2> errors.log
echo `date` "update_data.sh terminated unexpectedly!!"
sleep 3
done

