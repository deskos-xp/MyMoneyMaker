#! /usr/bin/env python3
from Client import main
import subprocess
from pathlib import Path
import json
import os
import argparse

class parseable:
    def __init__(self):
        parser=argparse.ArgumentParser()
        



def read_config():
    cmd=""
    config="startServer.json"
    with open(Path(config),"r") as fd:
        cmd=json.load(fd).get("cmd")
    return cmd.split(" ")

def launch_server():
    return subprocess.Popen(read_config(),shell=False,universal_newlines=True)
#print(launch_server())

server=launch_server()
code=main(server_pid=server.pid)
#if code == None:
os.kill(server.pid,9)

