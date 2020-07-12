from PyQt5.QtCore import QObject,QRunnable,QObject,QThread,QThreadPool
from PyQt5.QtWidgets import QApplication,QMainWindow,QErrorMessage
from PyQt5 import uic
from PyQt5.QtGui import QIcon,QPixmap,QImage
from .Loggin.Login import Login
from .MenuBar.MenuBar import MenuBar
from .Review.Review import Review
from .NewEntry.NewEntry import NewEntry
from .Charting.Charting import Charting
import os,sys,json
from pathlib import Path

from .About.workers.readAbout import readAbout
from .Update.Update import Update
from .MainWindow.default_fields import *

class Main(QMainWindow):
    def __init__(self,**kwargs):
        super(Main,self).__init__()
        
        self.cmdline=kwargs.get("cmdline")
        print(self.cmdline.options.server_start_config)
        self.server_pid=kwargs.get("server_pid")
        uic.loadUi("Client/MainWindow/forms/main.ui",self)
        self.statusBar().showMessage("server started on pid: {pid}".format(**dict(pid=self.server_pid)))
        self.stacks=dict()
        self.user=dict()
        self.stacks['login']=Login(self,self.cmdline)
        
        def store(var):
            for i in self.stacks.keys():
                if i != "login":
                    self.stacks[i].auth=var
                if i == "charting":
                    self.stacks[i].clearGraph()
                    self.stacks[i].rechart()
        self.stacks['login'].signals.hasUser.connect(store)

        self.stacks['reviewlast']=Review(self.stacks['login'].user,self)
        self.stacks['newEntry']=NewEntry(self)
        self.stacks['charting']=Charting(self)
        self.stacks['update']=Update(self)
        self.stacks['menubar']=MenuBar(self)
        #self.menubar=MenuBar(self)

        self.about=readAbout(Path("Client/MainWindow/about.json"))
        self.about.signals.finished.connect(lambda :print("finished reading about"))
        #not this one
        self.about.signals.hasError.connect(lambda x:QErrorMessage(self).showMessage(str(x)+__name__))
        QThreadPool.globalInstance().start(self.about)

        def update_window(data):
            windowIcon=QIcon(QPixmap(str(Path("Client/MainWindow")/Path(data.get("logo")))))
            self.setWindowIcon(windowIcon)
            self.setWindowTitle(data.get("name"))

        self.about.signals.hasAbout.connect(update_window)

        #self.setWindowIcon(QIcon(QPixmap(str(Path("Client/MainWindow/program.png")))))
        print(self.user,"user"*10)
        self.show()

def main(**kwargs):
    app=QApplication(sys.argv)
    win=Main(**kwargs)
    app.exec_()
