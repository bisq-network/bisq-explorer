###########################################
#                                         #
#  Copyright Grazcoin 2017                #
#  https://github.com/grazcoin/bisq-tools #
#                                         #
###########################################

# globals.py

# rpc_user and rpc_password
from rpc_passwd import *
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


def init():
    global rpc_connection
    global last_block
    global d # debug mode
    global bsqutxo_dict
    global bsqo_dict
    global tx_dict
    global addr_dict
    last_block=0
    rpc_connection=AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(rpc_user, rpc_password))
    bsqutxo_dict={}
    bsqo_dict={}
    tx_dict={}
    addr_dict={}
    d=False

