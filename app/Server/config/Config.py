import json,os
from pathlib import Path


class Config:
    def getDict(self,path:Path):
        d={}
        with open(path,"r") as fd:
            d=json.load(fd)
        return d
    path=Path("Server/config/env.json")
    def __init__(self,path:Path=None):
        if not path:
            path=self.path
        d=self.getDict(path)
        for i in d.keys():
            self.__dict__[i]=d[i]
