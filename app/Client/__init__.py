from PyQt5.QtCore import QObject,QRunnable,QObject,QThread,QThreadPool
from PyQt5.QtWidgets import QApplication,QMainWindow
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

class Main(QMainWindow):
    def __init__(self):
        super(Main,self).__init__()

        uic.loadUi("Client/MainWindow/forms/main.ui",self)
       
        self.stacks=dict()
        self.user=dict()
        self.stacks['login']=Login(self)
        def store(var):
            for i in self.stacks.keys():
                if i != "login":
                    self.stacks[i].auth=var

        self.stacks['login'].signals.hasUser.connect(store)

        self.stacks['reviewlast']=Review(self.stacks['login'].user,self)
        self.stacks['newEntry']=NewEntry(self)
        self.stacks['charting']=Charting(self)
        self.menubar=MenuBar(self)

        self.about=readAbout(Path("Client/MainWindow/about.json"))
        self.about.signals.finished.connect(lambda :print("finished reading about"))
        self.about.signals.hasError.connect(lambda x:print(x))
        QThreadPool.globalInstance().start(self.about)

        def update_window(data):
            windowIcon=QIcon(QPixmap(str(Path("Client/MainWindow")/Path(data.get("logo")))))
            self.setWindowIcon(windowIcon)
            self.setWindowTitle(data.get("name"))

        self.about.signals.hasAbout.connect(update_window)

        #self.setWindowIcon(QIcon(QPixmap(str(Path("Client/MainWindow/program.png")))))
        print(self.user,"user"*10)
        self.show()


def main():
    app=QApplication(sys.argv)
    win=Main()
    app.exec_()
