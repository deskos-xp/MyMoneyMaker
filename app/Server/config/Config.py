import json,os
from pathlib import Path
def cp(root_conf:Path,user_conf:Path):
        with open(root_conf,"r") as fd_in,open(user_conf,"w") as fd_out:
            json.dump(json.load(fd_in),fd_out)


def server_config():
    path=Path("Server/config/env.json")
    if os.getuid() != 0:
        if not Path(Path().home() / Path(".cache/mymoneymaker_env.json")).exists():
            cp(path,Path(Path().home() / Path(".cache/mymoneymaker_env.json")))
        path=Path(Path().home() / Path(".cache/mymoneymaker_env.json"))
    return path

class Config:
    def getDict(self,path:Path):
        d={}
        with open(path,"r") as fd:
            d=json.load(fd)
        return d
    def __init__(self,path:Path=None):
        path=server_config()           
        if not path:
            path=self.path
        d=self.getDict(path)
        for i in d.keys():
            if i == "LOG":
                self.__dict__[i]=Path.home() / Path(d.get(i))
            else:
                self.__dict__[i]=d[i]
