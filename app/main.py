#! /usr/bin/env python3
from Client import main
import subprocess
from pathlib import Path
import json
import os
import argparse
import Parser       

class dummy:
    def __init__(self,**kwargs):
        for k in kwargs.keys():
            self.__dict__[k]=kwargs[k]

def read_config(**kwargs):
    cmd={}
    config="startServer.json"
    cmd_opt=kwargs.get("override")
    if 'server_start_config' in cmd_opt.__dict__.keys():
        config=cmd_opt.__dict__.get("server_start_config")

    total_cmd=[]
    with open(Path(config),"r") as fd:
        cmd=json.load(fd)
    args={ i[0]:i[1] for i in cmd_opt._get_kwargs()}
    overridden=[]
    for k in cmd.keys():
        override=False
        if args.get("cmd") == "adjust-flask":
            if k in ['protocol','port']:
                if k == 'protocol':
                    total_cmd.append("--{proto}".format(**dict(proto=str(args.get(k)))))
                elif k == 'port':
                    total_cmd.append(":{port}".format(**dict(port=str(args.get(k)))))
                overridden.append(k)
        if k not in overridden:    
            total_cmd.append(str(cmd.get(k)))
    return total_cmd

def launch_server(**kwargs):
    return subprocess.Popen(read_config(**kwargs),shell=False,universal_newlines=True)

p=Parser.parser()
server=dummy(pid=0)
if not p.options.no_flask:
    server=launch_server(override=p.options)
code=main(server_pid=server.pid,cmdline=p)
if server.pid not in [None,0,[],{}]:
    print(server.pid)
    os.kill(server.pid,9)
'''
p=Parser.parser()
print(read_config(override=p.options))
'''
