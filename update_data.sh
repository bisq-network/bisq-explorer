#!/bin/bash

DATADIR=/home/user/.local/share/seed_BTC_TESTNET_p66zj5dzhccqhes3/btc_testnet/db


rsync -r $DATADIR/db/ www/data
python bsq_json.py
