#!/usr/bin/python

###########################################
#                                         #
#  Copyright Grazcoin 2017                #
#  https://github.com/grazcoin/bisq-tools #
#                                         #                                         
###########################################

import subprocess
import inspect
import simplejson
import time
import git
import os
import bsq_globals

def run_command(command, input_str=None, ignore_stderr=False):
    if ignore_stderr:
        if input_str!=None:
            p = subprocess.Popen(command, shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)
            return p.communicate(input_str)
        else:
            p = subprocess.Popen(command, shell=True,
                stdout=subprocess.PIPE)
            return p.communicate()
    else:
        if input_str!=None:
            p = subprocess.Popen(command, shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            return p.communicate(input_str)
        else:
            p = subprocess.Popen(command, shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            return p.communicate()

def error(msg):
    last_block_msg=''
    func_name='unknown'
    try:
        func_name=inspect.stack()[1][3]
    except IndexError:
        pass
    # on parse: update last block
    if func_name.startswith('parse'):
        # store last parsed block
        try:
            last_block_msg='('+str(bsq_globals.last_block)+')'
        except IOError:
            pass
    print '[E] '+func_name+': '+str(msg)+last_block_msg
    exit(1)

def info(msg):
    func_name='unknown'
    try:
        func_name=inspect.stack()[1][3]
    except IndexError:
        pass
    print '[I] '+func_name+': '+str(msg)

def debug(msg):
    if bsq_globals.d == True:
        func_name='unknown'
        try:
            func_name=inspect.stack()[1][3]
        except IndexError:
            pass
        print '[D] '+func_name+': '+str(msg)

def formatted_decimal(float_number):
    s=str("{0:.8f}".format(float_number))
    if s.strip('0.') == '':      # only zero and/or decimal point
        return '0.0'
    else:
        trimmed=s.rstrip('0')     # remove zeros on the right
        if trimmed.endswith('.'): # make sure there is at least one zero on the right
            return trimmed+'0'
        else:
            if trimmed.find('.')==-1:
                return trimmed+'.0'
            else:
                return trimmed

def format_time_from_struct(st, short=False):
    if short:
        return time.strftime('%Y%m%d',st)
    else:
        return time.strftime('%d %b %Y %H:%M:%S GMT',st)

def format_time_from_epoch(epoch, short=False):
    return format_time_from_struct(time.localtime(int(epoch)), short)

def get_now():
    return format_time_from_struct(time.gmtime())

def get_today():
    return format_time_from_struct(time.gmtime(), True)

def get_string_xor(s1,s2):
    result = int(s1, 16) ^ int(s2, 16)
    return '{:x}'.format(result)

def load_dict_from_file(filename, all_list=False, skip_error=False):
    tmp_dict={}
    try:
        f=open(filename,'r')
        if all_list == False:
            tmp_dict=simplejson.load(f)[0]
        else:
            tmp_dict=simplejson.load(f)
        f.close()
    except IOError: # no such file?
        if skip_error:
            info('dict load failed. missing '+filename)
        else:
            error('dict load failed. missing '+filename)
    return tmp_dict

# mkdir -p function
def mkdirp(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)

# dump json to a file, and replace it atomically
def atomic_json_dump(tmp_dict, filename, add_brackets=True):
    # check if filename already exists
    # if exists, write to a tmp file first
    # then move atomically

    # make sure path exists
    path, only_filename = os.path.split(filename)
    mkdirp(path)

    f=open(filename,'w')
    if add_brackets:
        f.write('[')
    f.write(simplejson.dumps(tmp_dict, sort_keys=True, use_decimal=True))
    if add_brackets:
        f.write(']')
    f.write('\n')
    f.close()

def load_json_file(filename):
    f=open(filename,'r')
    json_data=f.read()
    f.close()
    data=simplejson.loads(unicode(json_data))
    return data

def get_git_details(directory="~/github"):
    repo = git.Repo(directory)
    assert repo.bare == False
    head_commit=repo.head.commit
    timestamp=format_time_from_epoch(int(head_commit.authored_date), True)
    return(head_commit.hexsha,timestamp)
