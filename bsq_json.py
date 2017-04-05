#!/usr/bin/python

###########################################
#                                         #
#  Copyright Grazcoin 2017                #
#  https://github.com/grazcoin/bisq-tools #
#                                         #                                         
###########################################

import logging
from bsq_utils_general import *
from bsq_utils_parse import *
import sys
from pprint import pprint

# debug and last_block:
import bsq_globals

bsq_globals.init()

bsq_globals.bsqo_dict=load_json_file('www/general/bsq_txos.json')


for k in bsq_globals.bsqo_dict.keys():
    if bsq_globals.bsqo_dict[k][u'bsqAmount']==0:
        bsq_globals.bsqo_dict.pop(k)
        print "drop:",k
        continue

    txid=k.split(':')[0]
    genesis=bsq_globals.bsqo_dict[k].has_key(u'icon') and bsq_globals.bsqo_dict[k][u'icon']=='exodus'
    update_outputs_for_tx(txid, genesis)

    # that's for address on the sending side
    is_spent=(bsq_globals.bsqo_dict[k][u'spentInfo']!=None)
    dest_addrs=bsq_globals.bsqo_dict[k][u'scriptPubKey']['addresses']
    for a in dest_addrs:
        if bsq_globals.addr_dict.has_key(a):
            if is_spent == False:
                bsq_globals.addr_dict[a][u'utxo'].update({k:bsq_globals.bsqo_dict[k]})
            else:
                bsq_globals.addr_dict[a][u'stxo'].update({k:bsq_globals.bsqo_dict[k]})
        else:
            bsq_globals.addr_dict[a]={u'utxo':{},u'stxo':{}} # for 
            if is_spent == False:
                bsq_globals.addr_dict[a][u'utxo']={k:bsq_globals.bsqo_dict[k]}
            else:
                bsq_globals.addr_dict[a][u'stxo']={k:bsq_globals.bsqo_dict[k]}

    atomic_json_dump(bsq_globals.bsqo_dict[k],'www/txo/'+k+'.json')


for k in bsq_globals.tx_dict.keys():
     print "################"

     bsq_received=0
     bsq_sent=0
     bsq_burnt=0

     txtxo={}
     tx_data=bsq_globals.tx_dict[k]
     vin_amount=len(tx_data[u'vin'])
     vin_keys_list=[]
     for i in range(vin_amount):
         txo_id=str(tx_data[u'vin'][i][u'txid'])+':'+str(tx_data[u'vin'][i][u'vout'])
         print i,k,txo_id
         # are there bsq on that txo?
         if bsq_globals.bsqo_dict.has_key(txo_id) and bsq_globals.bsqo_dict[txo_id].has_key(u'bsqAmount') and bsq_globals.bsqo_dict[txo_id][u'bsqAmount'] > 0:
             vin_keys_list.append(txo_id)
             # that's for addresses on the receiving side
#             src_addrs=bsq_globals.bsqo_dict[txo_id][u'scriptPubKey']['addresses']
#             for a in src_addrs:
#                 if bsq_globals.addr_dict.has_key(a):
#                     bsq_globals.addr_dict[a][u'vin'].update({txo_id:bsq_globals.bsqo_dict[txo_id]})
#                 else:
#                     bsq_globals.addr_dict[a]={u'vin':{},u'vout':{}} # for 
#                     bsq_globals.addr_dict[a][u'vin']={txo_id:bsq_globals.bsqo_dict[txo_id]}


#
     vin_keys_list.sort()

     vin_list=[]
     try:
         for vik in vin_keys_list:
             vin_list.append(bsq_globals.bsqo_dict[vik])
             bsq_received+=bsq_globals.bsqo_dict[vik][u'bsqAmount']
     except KeyError:
         print "KeyError:",vik

     vout_list=[]
     for i in range(len(tx_data[u'vout'])):
         vok=k+':'+str(i)
         try:
             if bsq_globals.bsqo_dict[vok].has_key(u'bsqAmount') and bsq_globals.bsqo_dict[vok][u'bsqAmount'] > 0:
                 vout_list.append(bsq_globals.bsqo_dict[vok])
                 bsq_sent+=bsq_globals.bsqo_dict[vok][u'bsqAmount']
         except KeyError:
             print "No bsq in:",vok
             pass

     bsq_burnt=bsq_received-bsq_sent

     bsq_globals.tx_dict[k][u'bsqReceived']=bsq_received
     bsq_globals.tx_dict[k][u'bsqSent']=bsq_sent
     bsq_globals.tx_dict[k][u'bsqBurnt']=bsq_burnt

     atomic_json_dump([vin_list,vout_list],"www/txtxos/txtxos-"+k+'.json', add_brackets=False)
     atomic_json_dump(bsq_globals.tx_dict[k],'www/tx/'+k+'.json')



sorted_tx_list=get_sorted_tx_list(reverse=True)
summary_list=[]

for t in sorted_tx_list:
    try:
        summary_list.append({u'txid':t[u'txid'], u'time':str(t[u'time'])+'000', u'bsqAmount':t[u'bsqSent'], u'toAddress':t[u'vout'][0][u'scriptPubKey'][u'addresses'][0], u'icon':t[u'vout'][0][u'icon'], u'color':t[u'vout'][0][u'color'], u'iconText':t[u'vout'][0][u'iconText']})
    except KeyError:
        print "BOOOOOOOOOOOOOOOOOOO!"
        print t


for i in range(int(len(summary_list)/10)+1):
    strnum=str(i+1).zfill(4)
    atomic_json_dump(summary_list[i*10:i*10+9],'www/general/BSQ_'+strnum+'.json', add_brackets=False)

# generate addresses json
for a in bsq_globals.addr_dict.keys():
    utxo_list=[]
    stxo_list=[]
    balance=0
    received_num=0
    spent=0
    spent_num=0
    burnt=0
    burnt_num=0
    genesis=0
    genesis_tx=0
    for u in bsq_globals.addr_dict[a][u'utxo'].items():
        utxo=u[1]
        txid,outputIndex=u[0].split(':')
        utxo[u'txid']=txid
        utxo[u'outputIndex']=outputIndex
        utxo_list.append(utxo)
        balance+=utxo[u'bsqAmount']
        if utxo[u'icon']=='exodus':
            genesis+=utxo[u'bsqAmount']
            genesis_tx+=1
        received_num+=1
    for s in bsq_globals.addr_dict[a][u'stxo'].items():
        stxo=s[1]
        txid,outputIndex=s[0].split(':')
        stxo[u'txid']=txid
        stxo[u'outputIndex']=outputIndex
        stxo_list.append(stxo)
        spent+=stxo[u'bsqAmount']
        if stxo[u'icon']=='exodus':
            genesis+=stxo[u'bsqAmount']
            genesis_tx+=1
        spent_num+=1

    # get burnt from all spent transactions
    stxos=bsq_globals.addr_dict[a][u'stxo'].keys()
    txs=set()
    for s in stxos:
        txs.add(s.split(':')[0])
    for tx in txs:
        if bsq_globals.tx_dict[tx][u'bsqBurnt']>0:
            burnt+=bsq_globals.tx_dict[tx][u'bsqBurnt']
            burnt_num+=1

    addr_json={u'address':a}
    addr_json.update({u'utxos':utxo_list})
    addr_json.update({u'stxos':stxo_list})
    addr_json.update({u'reserved':0})

    addr_json.update({u'balance':balance})
    addr_json.update({u'totalGenesis':genesis})
    addr_json.update({u'totalReceived':balance+spent})
    addr_json.update({u'totalSpent':spent})
    addr_json.update({u'totalBurnt':burnt})

    addr_json.update({u'totalReserved':0})
    addr_json.update({u'genesisTxNum':genesis_tx})
    addr_json.update({u'receivedOutputsNum':received_num+spent_num})
    addr_json.update({u'spentOutputsNum':spent_num})
    addr_json.update({u'burntNum':burnt_num})

    atomic_json_dump(addr_json,'www/addr/'+a+'.json', add_brackets=False)


for tx in bsq_globals.tx_dict.keys():
    if bsq_globals.tx_dict[tx][u'vout'][0][u'iconText']=="Genesis":
        bsq_globals.stats_dict['Minted amount']+=bsq_globals.tx_dict[tx][u'bsqSent']
    if bsq_globals.tx_dict[tx][u'bsqBurnt']>0:
        bsq_globals.stats_dict['Burnt amount']+=bsq_globals.tx_dict[tx][u'bsqBurnt']

bsq_globals.stats_dict['Existing amount']=bsq_globals.stats_dict['Minted amount']-bsq_globals.stats_dict['Burnt amount']

for txo in bsq_globals.bsqo_dict.keys():
    try:
        if bsq_globals.bsqo_dict[txo][u'spentInfo']==None:
            bsq_globals.stats_dict['Unspent TXOs']+=1
        else:
            bsq_globals.stats_dict['Spent TXOs']+=1
    except KeyError:
        print "Missing spentInfo field! ",txo

bsq_globals.stats_dict['Addresses']=len(bsq_globals.addr_dict.keys())
bsq_globals.stats_dict['Price']=0.00001234
bsq_globals.stats_dict['Marketcap']=bsq_globals.stats_dict['Price']*bsq_globals.stats_dict['Existing amount']


stats_json=[]
for k in ["Existing amount", "Minted amount", "Burnt amount", "Addresses", "Unspent TXOs", "Spent TXOs", "Price", "Marketcap"]:
    stats_json.append({"name":k, "value":bsq_globals.stats_dict[k]})

atomic_json_dump(stats_json,'www/general/stats.json', add_brackets=False)

