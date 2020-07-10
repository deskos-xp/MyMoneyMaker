from PyQt5 import uic
from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget
import os,sys,json
from pathlib import Path
import pyqtgraph as pg
from ..MainWindow.default_fields import *
from .workers.getEntries import getEntries
from PyQt5.QtGui import QIcon

class Charting(QWidget):
    def __init__(self,parent):
        self.parent=parent
        self.auth=dict()
        super(Charting,self).__init__()
        uic.loadUi("Client/MainWindow/forms/charting.ui",parent.charting)
        #parent.charting.graph=pg.PlotWidget(v)

        self.x=currency_lst()
        self.y=currency_lst()

        parent.charting.refresh.clicked.connect(self.rechart)
        parent.charting.refresh.setIcon(QIcon.fromTheme("refreshstructure"))
        parent.tabWidget.currentChanged.connect(self.rechart)
        parent.charting.refresh.click()
        parent.charting.clear.clicked.connect(self.clearGraph)
        parent.charting.clear.hide()

    def parseEntries(self,entries):
        #print(entries)
        e=entries.get("status")
        d=entries.get(e)
        self.x=currency_lst()
        self.y=currency_lst()
        for num,i in enumerate(d):
            total=currency_ut()
            for k in i.keys():
                if i.get(k) == None:
                    pass
                elif k == "pennies":
                    total['total']+=i[k]*0.01
                elif k == "nickels":
                    total['total']+=i[k]*0.05
                elif k == "dimes":
                    total['total']+=i[k]*0.10
                elif k == "quarters":
                    total['total']+=i[k]*0.25
                elif k == "dollar":
                    total['total']+=i[k]
                elif k == "dollar5":
                    total['total']+=i[k]*5
                elif k == "dollar10":
                    total['total']+=i[k]*10
                elif k == "dollar20":
                    total['total']+=i[k]*20
                elif k == "dollar50":
                    total['total']+=i[k]*50
                elif k == "dollar100":
                    total['total']+=i[k]*100
                if k in currency_mx().keys() and i.get(k) != None:
                    self.x[k].append(num)
                    self.y[k].append(i[k]*currency_mx()[k])
            self.x['total'].append(num)
            self.y['total'].append(total['total'])
        for i in currency_mx().keys():
            if i != "total":
                self.plot(self.x.get(i),self.y.get(i),update=True,name=i)
        self.plot(self.x.get("total"),self.y.get("total"),update=True)

    def clearGraph(self):
        self.parseEntries(dict(status="objects",objects=[currency_ut()]))

    def buildWorker(self):
        self.worker=getEntries(self.auth)
        self.worker.signals.finished.connect(lambda:print("finished getting values"))
        self.worker.signals.hasEntries.connect(self.parseEntries)
        self.worker.signals.hasError.connect(lambda x:print(x))
        self.worker.signals.hasResponse.connect(lambda x:print(x))

    def builderWorker(self):
        QThreadPool.globalInstance().start(self.worker)

    def rechart(self):
        #if not self.__dict__.get("worker"):
        self.buildWorker()

        if self.worker.signals.isFinished == False:
            print("worker was killed")
            self.worker.signals.kill()
        print("called rechart")

        self.builderWorker()
        #self.plot(self.x[''],self.y,update=True)

    def plot(self,x,y,update=False,name=None):
        if self.worker.signals.isFinished == False:
            return
        if name == None:
            if update == False:
                self.parent.charting.graph.plot(x,y,pen=(1,3))
            else:
                self.parent.charting.graph.plot(x,y,clear=True,pen=(1,3))
        else:
            try:
                n="graph_{name}".format(**dict(name=name))
                getattr(self.parent.charting,n).plot(x,y,pen=(1,3),clear=True)
            except Exception as e:
                print(e)


