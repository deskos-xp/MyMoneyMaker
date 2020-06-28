from PyQt5 import uic
from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget
import os,sys,json
from pathlib import Path
import pyqtgraph as pg
from .workers.getEntries import getEntries

class Charting(QWidget):
    def __init__(self,parent):
        self.parent=parent
        self.auth=dict()
        super(Charting,self).__init__()
        uic.loadUi("Client/MainWindow/forms/charting.ui",parent.charting)
        #parent.charting.graph=pg.PlotWidget(v)

        self.x=[] 
        self.y=[]

        parent.charting.refresh.clicked.connect(self.rechart)
        self.rechart()

    def parseEntries(self,entries):
        e=entries.get("status")
        d=entries.get(e)
        self.x.clear()
        self.y.clear()
        for num,i in enumerate(d):
            total=0
            for k in i.keys():
                if i.get(k) == None:
                    pass
                elif k == "pennies":
                    total+=i[k]*0.01
                elif k == "nickels":
                    total+=i[k]*0.05
                elif k == "dimes":
                    total+=i[k]*0.10
                elif k == "quarters":
                    total+=i[k]*0.25
                elif k == "dollar":
                    total+=i[k]
                elif k == "dollar5":
                    total+=i[k]*5
                elif k == "dollar10":
                    total+=i[k]*10
                elif k == "dollar20":
                    total+=i[k]*20
                elif k == "dollar50":
                    total+=i[k]*50
                elif k == "dollar100":
                    total+=i[k]*100
            self.x.append(num)
            self.y.append(total)
        print(self.x,self.y)
        self.plot(self.x,self.y,update=True)

    def builderWorker(self):
        self.worker=getEntries(self.auth)
        self.worker.signals.finished.connect(lambda:print("finished getting values"))
        self.worker.signals.hasEntries.connect(self.parseEntries)
        self.worker.signals.hasError.connect(lambda x:print(x))
        self.worker.signals.hasResponse.connect(lambda x:print(x))
        QThreadPool.globalInstance().start(self.worker)

    def rechart(self):
        print("called rechart")
        self.builderWorker()
        self.plot(self.x,self.y,update=True)

    def plot(self,x,y,update=False):
        if update == False:
            self.parent.charting.graph.plot(x,y,pen=(1,3))
        else:
            self.parent.charting.graph.plot(x,y,clear=True,pen=(1,3))



