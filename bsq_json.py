#!/usr/bin/python

###########################################
#                                         #
#  Copyright Grazcoin 2017                #
#  https://github.com/grazcoin/bisq-tools #
#                                         #
###########################################

import config
import logging
from bsq_utils_general import *
import sys
from pprint import pprint

# debug and last_block:
import bsq_globals

bsq_globals.init()
bsq_globals.chainstate_dict=load_json_file('www/data/json/all/blocks.json')

lines_per_page=10

lines=[]
last_block=0
for block in bsq_globals.chainstate_dict[u'blocks']:
    last_block=block[u'height']
    for tx in block[u'txs']:
        txid=tx[u'id']
        time=tx[u'time']
        txType=tx[u'txType']
        burntFee=tx[u'burntFee']
        outputsNum=0
        txBsqAmount=0
        # take address from first output as tx details
        address=tx[u'outputs'][0][u'address']

        if txType == 'UNVERIFIED':
            txTypeDisplayString='Unverified'
        elif txType == 'INVALID':
            txTypeDisplayString='Invalid'
        elif txType == 'GENESIS':
            txTypeDisplayString='Genesis'
        elif txType == 'TRANSFER_BSQ':
            txTypeDisplayString='Transfer BSQ'
        elif txType == 'PAY_TRADE_FEE':
            txTypeDisplayString='Pay trade fee'
        elif txType == 'PROPOSAL':
            txTypeDisplayString='Proposal'
        elif txType == 'COMPENSATION_REQUEST':
            txTypeDisplayString='Compensation request'
        elif txType == 'REIMBURSEMENT_REQUEST':
            txTypeDisplayString='Reimbursement request'
        elif txType == 'BLIND_VOTE':
            txTypeDisplayString='Blind vote'
        elif txType == 'VOTE_REVEAL':
            txTypeDisplayString='Vote reveal'
        elif txType == 'LOCKUP':
            txTypeDisplayString='Lockup'
        elif txType == 'UNLOCK':
            txTypeDisplayString='Unlock'
        else:
            txTypeDisplayString='Undefined'

        for o in tx[u'outputs']:
            index=o[u'index']
            if (not o.has_key(u'opReturn')):
                bsqAmount = o[u'bsqAmount']
                txBsqAmount += bsqAmount
                addr=o[u'address']
                unspent=o[u'isUnspent']
                outputsNum+=1
                txo_entry={u'bsqAmount':bsqAmount, u'time':time, u'txType':txType, u'txTypeDisplayString':txTypeDisplayString, u'txId':txid, u'index':str(index)}
                if bsq_globals.addr_dict.has_key(addr):
                    if unspent==True:
                        bsq_globals.stats_dict['Unspent TXOs']+=1
                        if bsq_globals.addr_dict[addr].has_key(u'utxos'):
                            bsq_globals.addr_dict[addr][u'utxos'].append(txo_entry)
                        else:
                            bsq_globals.addr_dict[addr][u'utxos']=[txo_entry]
                    else:
                        bsq_globals.stats_dict['Spent TXOs']+=1
                        if bsq_globals.addr_dict[addr].has_key(u'stxos'):
                            bsq_globals.addr_dict[addr][u'stxos'].append(txo_entry)
                        else:
                            bsq_globals.addr_dict[addr][u'stxos']=[txo_entry]

                else:
                    if unspent==True:
                        bsq_globals.stats_dict['Unspent TXOs']+=1
                        bsq_globals.addr_dict[addr]={u'utxos':[txo_entry]}
                    else:
                        bsq_globals.stats_dict['Spent TXOs']+=1
                        bsq_globals.addr_dict[addr]={u'stxos':[txo_entry]}

                if (o[u'txOutputType'] == 'GENESIS_OUTPUT' or
                        o[u'txOutputType'] == 'ISSUANCE_CANDIDATE_OUTPUT') and \
                        o[u'isVerified'] == True:
                    # collect minted coins for stats
                    bsq_globals.stats_dict['Minted amount']+=o[u'bsqAmount']

        # collect the fee for stats
        bsq_globals.stats_dict['Burnt amount']+=float(tx[u'burntFee'])

        line_dict={u'bsqAmount':txBsqAmount, u'txType':txType, u'txTypeDisplayString':txTypeDisplayString, u'txId':txid, u'time':time, u'burntFee':burntFee, u'outputsNum':outputsNum, u'height':last_block}
        lines.append(line_dict)

# divide by 100 Satoshi/BSQ (1 BSQ = 100 Sat)
bsq_globals.stats_dict['Minted amount']/=100
bsq_globals.stats_dict['Burnt amount']/=100
bsq_globals.stats_dict['Existing amount']/=100

# calculate more stats
# TODO missing issued amount
bsq_globals.stats_dict['Existing amount']=bsq_globals.stats_dict['Minted amount']-bsq_globals.stats_dict['Burnt amount']

bsq_globals.stats_dict['Addresses']=len(bsq_globals.addr_dict.keys())

# TODO not provided yet in jsons (though in app available)
# bsq_globals.stats_dict['Price']=0.001234
# bsq_globals.stats_dict['Marketcap']=bsq_globals.stats_dict['Price']*bsq_globals.stats_dict['Existing amount']


stats_json=[]
for k in ["Existing amount", "Minted amount", "Burnt amount", "Addresses", "Unspent TXOs", "Spent TXOs", "Price", "Marketcap"]:
   stats_json.append({"name":k, "value":bsq_globals.stats_dict[k]})
    
atomic_json_dump(stats_json,'www/general/stats.json', add_brackets=False)


# split recent tx to pages
lines.reverse()
pages=int((len(lines)-1)/lines_per_page)+1
for i in range(pages):
    strnum=str(i+1).zfill(4)
    atomic_json_dump(lines[i*lines_per_page:(i+1)*lines_per_page],'www/general/BSQ_'+strnum+'.json', add_brackets=False)

atomic_json_dump({"currency": "BSQ", "name": "BSQ token", "pages": pages},'www/values.json')


# update field in addr
for addr in bsq_globals.addr_dict.keys():
    balance=0
    totalReserved=0
    burntNum=0
    genesisTxNum=0
    receivedOutputsNum=0
    spentOutputsNum=0
    totalGenesis=0
    totalReceived=0
    totalSpent=0
    if bsq_globals.addr_dict[addr].has_key(u'utxos'):
        for u in bsq_globals.addr_dict[addr][u'utxos']:
            balance+=u[u'bsqAmount']
            if u[u'txType']=='GENESIS':
                genesisTxNum+=1
                totalGenesis+=u[u'bsqAmount']
            else:
                receivedOutputsNum+=1
                totalReceived+=u[u'bsqAmount']
    if bsq_globals.addr_dict[addr].has_key(u'stxos'):
        for s in bsq_globals.addr_dict[addr][u'stxos']:
            if s[u'txType']=='GENESIS':
                genesisTxNum+=1
                totalGenesis+=s[u'bsqAmount']
                spentOutputsNum+=1
                totalSpent+=s[u'bsqAmount']
            else:
                receivedOutputsNum+=1
                totalReceived+=s[u'bsqAmount']
                spentOutputsNum+=1
                totalSpent+=s[u'bsqAmount']

    totalBurnt=totalGenesis+totalReceived-totalSpent-balance

    bsq_globals.addr_dict[addr][u'address']=addr
    bsq_globals.addr_dict[addr][u'balance']=balance
    bsq_globals.addr_dict[addr][u'genesisTxNum']=genesisTxNum
    bsq_globals.addr_dict[addr][u'totalGenesis']=totalGenesis
    bsq_globals.addr_dict[addr][u'receivedOutputsNum']=receivedOutputsNum
    bsq_globals.addr_dict[addr][u'totalReceived']=totalReceived
    bsq_globals.addr_dict[addr][u'spentOutputsNum']=spentOutputsNum
    bsq_globals.addr_dict[addr][u'totalSpent']=totalSpent
    bsq_globals.addr_dict[addr][u'burntNum']=burntNum
    bsq_globals.addr_dict[addr][u'totalBurnt']=totalBurnt
    bsq_globals.addr_dict[addr][u'totalReserved']=totalReserved


for addr in bsq_globals.addr_dict.keys():
    atomic_json_dump(bsq_globals.addr_dict[addr],'www/addr/'+addr+'.json', add_brackets=False)

(commit_hexsha,commit_time)=get_git_details()
now=get_now()
revision_dict={"commit_hexsha":commit_hexsha, "commit_time":commit_time, "last_block":last_block, "last_parsed":now, "url":"https://github.com/bisq-network/bisq"}

atomic_json_dump(revision_dict,'www/revision.json', add_brackets=False)
