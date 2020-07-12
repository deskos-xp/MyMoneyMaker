from PyQt5.QtCore import QObject,QThread,QThreadPool,QRunnable,pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QDialog,QWidget,QCheckBox,QLineEdit,QTabWidget,QErrorMessage
from .workers.loginWorker import loginWorker
from .RememberMe.Remember import Remember
from pathlib import Path
import json
from copy import deepcopy
from ..MainWindow.default_fields import *
from PyQt5.QtGui import QIcon
from urllib.parse import urlparse
from ..About.workers.readAbout import readAbout
from ..About.workers.readIcon import readIcon
from pathlib import Path
from PyQt5.QtGui import QIcon,QPixmap
class LoginSignals(QObject):
    hasUser:pyqtSignal=pyqtSignal(dict)

class Login:
    def __init__(self,parent,cmdline):
        self.user=dict()
        self.parent=parent
        self.signals=LoginSignals()
        self.cmdline=cmdline
            
        self.auth=dict(host="",username="",password="")
        parent.username.textChanged.connect(self.storeValue)
        parent.password.textChanged.connect(self.storeValue)
        parent.host.textChanged.connect(self.storeValue)
        parent.loggin_btn.clicked.connect(self.login)
        parent.loggin_btn.setIcon(QIcon.fromTheme('lock'))
        self.wid=getattr(parent,'loggedIn')
        self.index_loggedIn=parent.stackedWidget.indexOf(self.wid)
        self.auth['username']=self.parent.username.text()
        self.auth['password']=self.parent.password.text()
        self.auth['host']=self.parent.host.text()
        self.cachedUser()
        self.aboutconfig()

    def setLogo(self,pixmap):
        self.parent.logo.setPixmap(pixmap)

    def icon(self,about):
        path=Path(Path("Client/MainWindow") / Path(about.get("logo")))
        self.icon_getter=readIcon(path)
        self.icon_getter.signals.hasError.connect(lambda x:QErrorMessage(self.parent).showMessage(str(x)))
        self.icon_getter.signals.hasPixmap.connect(self.setLogo)
        self.icon_getter.signals.finished.connect(lambda: print("finished getting logo"))
        QThreadPool.globalInstance().start(self.icon_getter)

    def aboutconfig(self):
        self.aboutconfigVar=readAbout(Path("Client/MainWindow/about.json"))
        self.aboutconfigVar.signals.hasError.connect(lambda x:QErrorMessage(self.parent).showMessage(str(x)))
        self.aboutconfigVar.signals.hasAbout.connect(self.icon)
        self.aboutconfigVar.signals.finished.connect(lambda : print("reading about config"))
        QThreadPool.globalInstance().start(self.aboutconfigVar)
    
    def cmdline_options(self):
        if self.cmdline != None:
            if self.cmdline.options.__contains__('port') and self.cmdline.options.__contains__("protocol"):
                #print(self.cmdline.options,"should not be None(port and scheme)")       
                #print(self.parent.host.text(),"should be adjusted!")
                parsed_uri=urlparse(self.parent.host.text())
                host=parsed_uri.netloc.split(":")
                #print(host)
                if host:
                    h=host[0]
                    replace="{scheme}://{addr}:{port}".format(**dict(scheme=self.cmdline.options.protocol,addr=h,port=self.cmdline.options.port))
                    #print(replace,"replaced")
                    self.parent.host.setText(replace)
            
            #print(parsed_uri,"uri"*10)

    def cachedUser(self):
        try:
            def hasUser(user):
                self.auth['username']=user.get("uname")
                self.auth['password']=user.get("password")
                self.auth['host']=user.get("host")
                self.parent.username.setText(user.get("uname"))
                self.parent.password.setText(user.get("password"))
                self.parent.host.setText(user.get("host"))
                self.cmdline_options()
                self.parent.rememberMe.setChecked(user.get("rememberMe"))

                self.signals.hasUser.emit(user)
                
            self.cached=Remember(self.parent,Path.home()/Path(".cache")/Path("User.json"))
            self.cached.signals.finished.connect(lambda :print("finished loading user from cache"))
            self.cached.signals.hasError.connect(lambda x:QErrorMessage(self.parent).showMessage(str(x)))
            self.cached.signals.hasUser.connect(hasUser)
            QThreadPool.globalInstance().start(self.cached)
        except Exception as e:
            print(e)

    def cacheUser(self,us):
        if self.parent.rememberMe.isChecked():
            u=deepcopy(us)
            u['rememberMe']=self.parent.rememberMe.isChecked()
            with open(Path.home()/Path(".cache")/Path("User.json"),"w") as fd:
                json.dump(u,fd)
        else:
            u=deepcopy(user())
            u['rememberMe']=self.parent.rememberMe.isChecked()
            with open(Path.home()/Path(".cache")/Path("User.json"),"w") as fd:
               json.dump(u,fd)
 
    def builderWorker(self):
        #x=QErrorMessage(self.parent)
        #x.showMessage(" message")
        self.loginWorker=loginWorker(self.auth)
        self.loginWorker.signals.hasUser.connect(self.success)
        self.loginWorker.signals.hasResponse.connect(lambda x:print(x))
        self.loginWorker.signals.hasError.connect(lambda x: QErrorMessage(self.parent).showMessage(str(x)))
        self.loginWorker.signals.finished.connect(lambda:print("finished attempting"))

    def success(self,user):
        #print(user,'success '*10)
        if user and user[0]:
            user=user[0]
            user['password']=self.auth.get("password")
            user['host']=self.auth.get("host")
            self.user=user
            self.signals.hasUser.emit(self.user)
            self.parent.stackedWidget.setCurrentIndex(self.index_loggedIn)
            self.cacheUser(user)
            self.parent.review.refresh.click()
        #print(self.user)


    def login(self):
        self.builderWorker()
        QThreadPool.globalInstance().start(self.loginWorker)
        #print(self.auth)
        

    def storeValue(self,text):
        self.auth[self.parent.sender().objectName()]=text
        #print(text)
