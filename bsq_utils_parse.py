#!/usr/bin/python

###########################################
#                                         #
#  Copyright Grazcoin 2017                #
#  https://github.com/grazcoin/bisq-tools #
#                                         #                                         
###########################################

import bsq_globals
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json

utxo_visited={}

# all available properties of a transaction
tx_properties=\
    ['txid', 'time', \
     'height', \
     'isIssuanceTx', \
     'bsq_sent', 'bsqReceived', 'bsqBurnt', \
     'addresses', \
     'icon', 'iconText', 'color', \
     'details', 'txTypeStr', \
     'status']

output_properties=\
    [u'txid', u'index', u'bsqAmount', u'spentInfo', u'validated']

# update the main tx database
# example call:
# update_tx_dict(txid, icon='default', color='bgc_done')
def update_tx_dict(txid, *arguments, **keywords):
    # txid is first arg
    # then come the keywords and values to be modified

    # is there already entry for this txid?
    if not tx_dict.has_key(txid):
        # no - so create a new one
        # remark: loading all tx for that txid
        tx_dict[txid]=load_dict_from_file('tx/'+txid+'.json', all_list=True)

    # get the update_fs from tx_dict for that tx
    if tx_dict[txid].has_key('update_fs'):
        update_fs=tx_dict[txid]['update_fs']
    else:
        # start with default "no need to update fs"
        tx_dict[txid]['update_fs']=False
        update_fs=False

    # update all given fields with new values
    keys = sorted(keywords.keys())
    # allow only keys from tx_properties
    for kw in keys:
        try:
            prop_index=tx_properties.index(kw)
        except ValueError:
            info('BUG: unsupported property of tx: '+kw)
            return False
        # set update_fs flag if necessary (if something really changed)
        try:
            update_fs = tx_dict[txid][kw]!=keywords[kw] or update_fs
        except KeyError:
            update_fs = True
        tx_dict[txid][kw]=keywords[kw]

    tx_dict[txid]['update_fs']=update_fs
    return True


# write back to fs all tx which got modified
def write_back_modified_tx():
    for k in tx_dict.keys():
        if tx_dict[k]['update_fs'] == True:
            # remove update fs marker
            del tx_dict[k]['update_fs']
            # save back to filesystem
            atomic_json_dump(tx_dict[k], 'tx/'+k+'.json', add_brackets=False)


def initial_tx_dict_load():
    # run on all files in tx
    tx_files=sorted_ls('tx')

    # load dict of each
    for filename in tx_files:
        if filename.endswith('.json'):
            txid=filename.split('.')[0]
            update_tx_dict(txid)


def get_sorted_tx_list(reverse=False):
    tx_list=[]
    for i in bsq_globals.tx_dict.items():
        tx_list.append(i[1])
    return sorted(tx_list, key=lambda k: k[u'height'], reverse=reverse)


def get_tx_json(txid):
    try:
        tx_json=bsq_globals.rpc_connection.getrawtransaction(txid,1)
        return tx_json
    except Exception as e:
        print "oops (get_tx_json):",e

def get_height():
    try:
        info=bsq_globals.rpc_connection.getinfo()
    except Exception as e:
        print "oops (get_height):",e
    return int(info[u'blocks'])


def get_inputs(txid):
    j=get_tx_json(txid)
    inputs=[]
    for v in j[u'vin']:
        index=v[u'vout']
        txid=v[u'txid']
        inputs.append(txid+':'+str(index))
    return inputs

def get_spent_json(txid,index):
    try:
        j=bsq_globals.rpc_connection.getspentinfo({"txid": txid, "index": index})
        #print j
        # for example -
        # request: 
        # rpc_connection.getspentinfo({"txid": "10085081b3c7eb3d15bc45eab9f8c4bd17a043f92928ea321f2705370bd44865", "index":1})
        # response:
        # {u'index': 0, u'height': 443660, u'txid': u'0c2d2ecfc2c6059a62c177d6c2800a269478439564ed915d648bba4c4aa4086c'}
    except JSONRPCException as e:
        if str(e) == "-5: Unable to get spent info":
            j=None
        else:
            print "Network issue?"
            # retry few times?
            j=None
    return j

def recursive_get_spent_tx(spent_dict, max_height):

    # start new inside each recursive branch
    utxo_visited={}

    # get txid,index
    try:
        txid=spent_dict[u'txid']
        index=spent_dict[u'index']
    except Exception as e:
        print "oops:",e,"for",spent_dict
        return

    try:
        height=spent_dict[u'height']
        # notify that tx is not processed now (height is in the future comparing to max_height)
        if height>max_height:
            #print "max height", max_height ,"reached for", spent_dict
            return

    except KeyError:
        print "no height in ",spent_dict

    try:
        key=txid+':'+str(index)
        if utxo_visited.has_key(key):
            #print 'already visited '+key+' ... skip.'
            pass
        else:
            j=get_spent_json(txid,index)
#            print key+' -> '+str(j)
#            print get_inputs(txid)
            utxo_visited[key]=True
            if bsq_globals.bsqo_dict.has_key(key):
                bsq_globals.bsqo_dict[key][u'spentInfo']=j
            else:
                bsq_globals.bsqo_dict[key]={u'spentInfo':j, u'txid':txid, u'index':index, u'validated':False}
            if j!=None:
                spent_txid=j[u'txid']
                spent_height=j[u'height']
                sj=get_tx_json(spent_txid)
                n=len(sj[u'vout'])
                for i in range(n):
                    recursive_get_spent_tx({u'txid': spent_txid, u'index': int(i), u'height':spent_height}, max_height)

    except Exception as e:
        print "oops (recursive):",e


def update_outputs_for_tx(txid, genesis=False):
    tx_json=get_tx_json(txid)


    if not bsq_globals.tx_dict.has_key(txid):
        bsq_globals.tx_dict[txid]=tx_json

    # run over all outputs and add them to bsqutxo_dict
    index=0
    for o in tx_json['vout']:
        # The format is:
        # {u'valueSat': 700000,
        # u'scriptPubKey': {u'reqSigs': 1, u'hex': u'76a914d95933afd27f70537bdd4eab383e8f6f91d72be788ac',
        # u'addresses': [u'1LpEVV576FBUvEbRfb5qPkngXoNfW1EgfM'],
        # u'asm': u'OP_DUP OP_HASH160 d95933afd27f70537bdd4eab383e8f6f91d72be7 OP_EQUALVERIFY OP_CHECKSIG',
        # u'type': u'pubkeyhash'},
        # u'value': Decimal('0.00700000'),
        # u'n': 0}

        # remarks:
        # addresses list might be longer than one - e.g. for BIP11

        bsqutxo_item=o # the item is the parsed output
        # add missing fields to parsed output

        if tx_json.has_key('height'):
            bsqutxo_item[u'height']=tx_json['height']
        else:
            if tx_json.has_key('block'):
                bsqutxo_item[u'height']=tx_json['block']
        bsqutxo_item[u'time']=str(tx_json['blocktime'])+'000'
        bsqutxo_item[u'coinBase']=False # Zero chance for a SQU in a block generation tx

        bsqutxo_item[u'outputIndex']=index
        bsqutxo_item[u'status']="done"
        bsqutxo_item[u'invalid']=False

        if genesis==True:
            # mark as SQU genesis address
            bsqutxo_item[u'isIssuanceTx']=True # SQU directly from a genesis address

            # get amount of SQU
            bsqutxo_item[u'bsqAmount']=o[u'valueSat']

            # add spent info
            bsqutxo_item[u'spentInfo']=get_spent_json(txid,index)

            # icon
            bsqutxo_item[u'icon']="genesis"
            bsqutxo_item[u'iconText']="Genesis"
            bsqutxo_item[u'color']="bgc-new"
            bsqutxo_item[u'txTypeStr']="Genesis transaction"
        else:
            # icon
            bsqutxo_item[u'icon']="simplesend"
            bsqutxo_item[u'iconText']="Value transfer"
            bsqutxo_item[u'color']="bgc-new"
            bsqutxo_item[u'txTypeStr']="Token send"

        bsqutxo_item[u'transactionVersion']='0001'

        # add the item to a dict with key txid:index
        key=unicode(txid+':'+str(index))
        if bsq_globals.bsqo_dict.has_key(key):
            bsq_globals.bsqo_dict[key].update(bsqutxo_item)  # unspent dict
        else:
            bsq_globals.bsqo_dict[key]=bsqutxo_item
        index+=1
