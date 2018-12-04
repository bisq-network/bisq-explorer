#!/bin/bash

DATADIR=/home/sqrrm/.local/share/dao_test/seed_2002/btc_regtest


rsync -r $DATADIR/db/ www/data
python bsq_json.py
