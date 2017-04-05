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

genesis_txids_list=['10085081b3c7eb3d15bc45eab9f8c4bd17a043f92928ea321f2705370bd44865','9249e46293eac9b43d43468035ca41d48bf92ff07871e07e7f9bb4aecdfc2d8c','6d39423c64952b9d62b945f2496055d292fe10d7531d7069e84e2e76a7b8b836']

#max_height=444444
max_height=get_height()

blocks_chunk_size=1000

# preparing initial bsqo from genesis (and compensation requests)
for genesis_txid in genesis_txids_list:
    update_outputs_for_tx(genesis_txid, True)


print "running ..."

chunk_num=1
# get the starting height (look for minimal height among all outputs)
parse_height=max_height
for k in bsq_globals.bsqo_dict.keys():
    if bsq_globals.bsqo_dict[k][u'height'] != 0:
        parse_height=min(parse_height,bsq_globals.bsqo_dict[k][u'height'])

print "Starting height is:",parse_height, "and chunk size is:", blocks_chunk_size


# run in height chunks generate:
# 1. updated bsqo set until each height chunk, based on existing bsqo set
# 2. validate bsqo set, and drop invalid bsqo
# repeat for next chunk until max_height

while parse_height <= max_height:

    # the closest next "round" chunk
    parse_height=parse_height+blocks_chunk_size-parse_height%blocks_chunk_size

    keys=bsq_globals.bsqo_dict.keys()
    keys.sort()

    print
    print "#######################"
    print "##### upto",parse_height,"#####"
    print "#######################"

    for k in keys:

        # run recursively from each genesis output
        current={}
        txid,index=k.split(':')
        if bsq_globals.bsqo_dict[k].has_key(u'height'):
            height=bsq_globals.bsqo_dict[k][u'height']
        else:
            height=0
        recursive_get_spent_tx({u'txid': txid, u'index': int(index), u'height':height}, parse_height)

    # validate (drop invalid bsqo)
    outputs_list=bsq_globals.bsqo_dict.keys()
    outputs_list.sort()
    print "--------------------------------------------------------------------------------"
    print "starting with output set:",outputs_list
    print "--------------------------------------------------------------------------------"
    for current_key in outputs_list:
        #print current_key
        # skip calculation/validation of bsqAmount input if already exists
        if bsq_globals.bsqo_dict[current_key].has_key(u'bsqAmount'):
            #print "already bsqAmount there:",bsq_globals.bsqo_dict[current_key][u'bsqAmount'],"from:",current_key
            bsq_input=bsq_globals.bsqo_dict[current_key][u'bsqAmount']
        else:
            txid,index=current_key.split(':')
            sj=get_tx_json(txid)
            outputs_len=len(sj[u'vout'])
            inputs_len=len(sj[u'vin'])
            print "#####"
            print txid, "inputs:", inputs_len, "outputs:", outputs_len
            # sum bsq from all inputs
            bsq_input=0
            for i in range(inputs_len):
                input_txid=sj[u'vin'][i][u'txid']
                input_index=sj[u'vin'][i][u'vout']
                input_key=unicode(input_txid+':'+str(input_index))
                print "Calculating inputs from:",input_key
                if bsq_globals.bsqo_dict.has_key(input_key):
                    try:
                        print "Added SQU to input:",bsq_globals.bsqo_dict[input_key][u'bsqAmount']
                        bsq_input+=bsq_globals.bsqo_dict[input_key][u'bsqAmount']
                    except KeyError:
                        print "No SQU field on input key:",input_key
                        pass
                else:
                    print "No SQU on:",input_key
                    pass

            print "total bsq_input for",txid,"is",bsq_input
            #print "-----"

            bsq_input_left=int(bsq_input)
            for o in range(outputs_len):
                #print o
                output_key=unicode(txid+':'+str(o))
                requested_bsq_output=int(sj[u'vout'][o][u'valueSat'])
                if requested_bsq_output <= bsq_input_left: # enough SQU to fund new output
                    try:
                        bsq_globals.bsqo_dict[output_key][u'bsqAmount']=requested_bsq_output
                        bsq_globals.bsqo_dict[output_key][u'validated']=True
                        bsq_input_left-=requested_bsq_output
                        print "just used",requested_bsq_output,"granted to",output_key
                    except KeyError as e:
                        print "!!!!!!!!!!!!!!!!! KeyError",e
                    #print bsq_globals.bsqo_dict[output_key]
                else:
                    print "Out of SQU. Ignore request:",requested_bsq_output,"left:",bsq_input_left
                    #print bsq_globals.bsqo_dict[output_key]
                    try:
                        bsq_globals.bsqo_dict[output_key][u'bsqAmount']=0
                        bsq_globals.bsqo_dict[output_key][u'validated']=True
                    except KeyError as e:
                        print "!!!!!!!!!!!!!!111 KeyError",e
                    bsq_input_left=0 # first failure means the rest SQU are lost

    chunk_num+=1



atomic_json_dump(bsq_globals.bsqo_dict,'www/general/bsq_txos.json', add_brackets=False)
