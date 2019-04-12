###########################################
#                                         #
#  Copyright Bisq 2018                    #
#                                         #
###########################################

# globals.py

# rpc_user and rpc_password
from config import *
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


def init():
    global rpc_connection
    global last_block
    global d # debug mode
    global bsqutxo_dict
    global bsqo_dict
    global tx_dict
    global addr_dict
    global stats_dict
    global chainstate_dict
    last_block=0
    rpc_connection=AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user, rpc_password,rpc_host,rpc_port))
    bsqutxo_dict={}
    bsqo_dict={}
    tx_dict={}
    addr_dict={}
    stats_dict={"Existing amount":0,
            "Minted amount":0,
            "Burnt amount":0,
            "Addresses":0,
            "Unspent TXOs":0,
            "Spent TXOs":0,
            "Price":0,
            "Marketcap":0}
    chainstate_dict={}
    d=False

