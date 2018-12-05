#!/bin/bash

DATADIR=/home/user/.local/share/seedNode/btc_testnet

rm -rf www/data
cp -r $DATADIR/db www/data
rm -rf www/addr
python bsq_json.py
