#!/bin/bash

DATADIR=/home/user/.local/share/seed_BTC_TESTNET_p66zj5dzhccqhes3/btc_testnet

cd `dirname $0`
rm -rf www/data
rm -rf www/addr
cp -r $DATADIR/db www/data
python bsq_json.py
