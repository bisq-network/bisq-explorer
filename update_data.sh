#!/bin/bash

DATADIR=/home/user/.local/share/seed_BTC_TESTNET_p66zj5dzhccqhes3/btc_testnet

rsync -r $DATADIR/db/ www/data
rm -rf www/addr
python bsq_json.py
