#!/bin/bash

#DATADIR=/home/user/.local/share/seed_BTC_TESTNET_p66zj5dzhccqhes3/btc_testnet
DATADIR=/home/sqrrm/.local/share/dao_test/seed_2002/btc_regtest

cd `dirname $0`
rm -rf www/data
rm -rf www/addr
cp -r $DATADIR/db www/data
python bsq_json.py
