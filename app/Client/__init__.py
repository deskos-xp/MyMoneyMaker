from PyQt5.QtCore import QObject,QRunnable,QObject,QThread,QThreadPool
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5 import uic
from .Loggin.Login import Login
import os,sys,json

class Main(QMainWindow):
    def __init__(self):
        super(Main,self).__init__()

        uic.loadUi("Client/MainWindow/forms/main.ui",self)
        
        self.stacks=list()
        self.stacks.append(Login(self))

        self.show()


def main():
    app=QApplication(sys.argv)
    win=Main()
    app.exec_()
