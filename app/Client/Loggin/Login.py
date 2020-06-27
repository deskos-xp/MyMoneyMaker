from PyQt5.QtCore import QObject,QThread,QThreadPool,QRunnable,pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QDialog,QWidget,QCheckBox,QLineEdit,QTabWidget
from .workers.loginWorker import loginWorker
from .RememberMe.Remember import Remember
from pathlib import Path
import json
from copy import deepcopy
from ..MainWindow.default_fields import *

class LoginSignals(QObject):
    hasUser:pyqtSignal=pyqtSignal(dict)

class Login:
    def __init__(self,parent):
        self.user=dict()
        self.parent=parent
        self.signals=LoginSignals()

        self.auth=dict(host="",username="",password="")
        parent.username.textChanged.connect(self.storeValue)
        parent.password.textChanged.connect(self.storeValue)
        parent.host.textChanged.connect(self.storeValue)
        parent.loggin_btn.clicked.connect(self.login)

        self.wid=getattr(parent,'loggedIn')
        self.index_loggedIn=parent.stackedWidget.indexOf(self.wid)
        self.auth['username']=self.parent.username.text()
        self.auth['password']=self.parent.password.text()
        self.auth['host']=self.parent.host.text()
        self.cachedUser()

    def cachedUser(self):
        try:
            def hasUser(user):
                self.auth['username']=user.get("uname")
                self.auth['password']=user.get("password")
                self.auth['host']=user.get("host")
                self.parent.username.setText(user.get("uname"))
                self.parent.password.setText(user.get("password"))
                self.parent.host.setText(user.get("host"))
                self.parent.rememberMe.setChecked(user.get("rememberMe"))

                self.signals.hasUser.emit(user)
                
            self.cached=Remember(self.parent,Path("User.json"))
            self.cached.signals.finished.connect(lambda :print("finished loading user from cache"))
            self.cached.signals.hasError.connect(lambda x:print(x))
            self.cached.signals.hasUser.connect(hasUser)
            QThreadPool.globalInstance().start(self.cached)
        except Exception as e:
            print(e)

    def cacheUser(self,us):
        if self.parent.rememberMe.isChecked():
            u=deepcopy(us)
            u['rememberMe']=self.parent.rememberMe.isChecked()
            with open(Path("User.json"),"w") as fd:
                json.dump(u,fd)
        else:
            u=deepcopy(user())
            u['rememberMe']=self.parent.rememberMe.isChecked()
            with open(Path("User.json"),"w") as fd:
               json.dump(u,fd)
 
    def builderWorker(self):
        self.loginWorker=loginWorker(self.auth)
        self.loginWorker.signals.hasUser.connect(self.success)
        self.loginWorker.signals.hasResponse.connect(lambda x:print(x))
        self.loginWorker.signals.hasError.connect(lambda x:print(x,"###"))
        self.loginWorker.signals.finished.connect(lambda:print("finished attempting"))

    def success(self,user):
        print(user,'success '*10)
        if user and user[0]:
            user=user[0]
            user['password']=self.auth.get("password")
            user['host']=self.auth.get("host")
            self.user=user
            self.signals.hasUser.emit(self.user)
            self.parent.stackedWidget.setCurrentIndex(self.index_loggedIn)
            self.cacheUser(user)
            self.parent.review.refresh.click()
        print(self.user)


    def login(self):
        self.builderWorker()
        QThreadPool.globalInstance().start(self.loginWorker)
        print(self.auth)

    def storeValue(self,text):
        self.auth[self.parent.sender().objectName()]=text
        print(text)
