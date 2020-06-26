from PyQt5.QtCore import QObject,QThread,QThreadPool,QRunnable,pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QDialog,QWidget,QCheckBox,QLineEdit,QTabWidget
from .workers.loginWorker import loginWorker

class Login:
    def __init__(self,parent):
        self.user=dict()
        self.parent=parent
        self.auth=dict(host="",username="",password="")
        parent.username.textChanged.connect(self.storeValue)
        parent.password.textChanged.connect(self.storeValue)
        parent.host.textChanged.connect(self.storeValue)
        parent.loggin_btn.clicked.connect(self.login)

        self.wid=getattr(parent,'loggedIn')
        self.index_loggedIn=parent.stackedWidget.indexOf(self.wid)

        
    def builderWorker(self):
        self.loginWorker=loginWorker(self.auth)
        self.loginWorker.signals.hasUser.connect(self.success)
        self.loginWorker.signals.hasResponse.connect(lambda x:print(x))
        self.loginWorker.signals.hasError.connect(lambda x:print(x,"###"))
        self.loginWorker.signals.finished.connect(lambda:print("finished attempting"))

    def success(self,user):
        #print(user)
        if user and user[0]:
            user=user[0]
            user['password']=self.auth.get("password")
            self.user=user
            self.parent.stackedWidget.setCurrentIndex(self.index_loggedIn)
        print(self.user)


    def login(self):
        self.builderWorker()
        QThreadPool.globalInstance().start(self.loginWorker)
        print(self.auth)

    def storeValue(self,text):
        self.auth[self.parent.sender().objectName()]=text
        print(text)
