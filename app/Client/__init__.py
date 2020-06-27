from PyQt5.QtCore import QObject,QRunnable,QObject,QThread,QThreadPool
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5 import uic
from .Loggin.Login import Login
from .MenuBar.MenuBar import MenuBar
from .Review.Review import Review
import os,sys,json

class Main(QMainWindow):
    def __init__(self):
        super(Main,self).__init__()

        uic.loadUi("Client/MainWindow/forms/main.ui",self)
       
        self.menubar=MenuBar(self)
        self.stacks=dict()
        self.user=dict()
        self.stacks['login']=Login(self)
        def store(var):
            for i in self.stacks.keys():
                if i != "login":
                    self.stacks[i].auth=var

        self.stacks['login'].signals.hasUser.connect(store)

        self.stacks['reviewlast']=Review(self.stacks['login'].user,self)
        print(self.user,"user"*10)
        self.show()


def main():
    app=QApplication(sys.argv)
    win=Main()
    app.exec_()
