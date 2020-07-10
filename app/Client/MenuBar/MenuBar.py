from ..About.About import About
from ..ServerSettings.ServerSettings import ServerSettings
import getpass
from ..User.UserDialog import UserDialog
from PyQt5.QtGui import QIcon
from ..MainWindow.default_fields import * 

class MenuBar:
    def __init__(self,parent):
        self.parent=parent
        parent.actionLogout.triggered.connect(self.invalidus)
        parent.actionLogout.setIcon(QIcon.fromTheme("lock"))

        parent.actionExit.triggered.connect(parent.close)
        parent.actionExit.setIcon(QIcon.fromTheme("application-exit"))

        parent.action_About.triggered.connect(self.about_)
        parent.action_About.setIcon(QIcon.fromTheme("help-about"))

        parent.action_Server_Settings.triggered.connect(self.serverSettings_)
        parent.action_Server_Settings.setIcon(QIcon.fromTheme("offline-settings"))

        parent.stackedWidget.currentChanged.connect(self.lock_action_logout)
        self.lock_action_logout(0)

        parent.actionUser.triggered.connect(self.user_)
        parent.actionUser.setIcon(QIcon.fromTheme("system-users"))

    def serverSettings_(self):
        dialog=ServerSettings("Server/config/env.json",self.parent)
        #dialog.show()

    def invalidus(self):
        loggin=self.parent.loggin
        index=self.parent.stackedWidget.indexOf(loggin)
        self.parent.stackedWidget.setCurrentIndex(index)
        self.parent.auth=dict()
        
        self.parent.stacks['login'].cachedUser()
        for stack in self.parent.stacks.keys():
            if stack == "Charting":
                for i in self.parent.stacks[stack].y.keys():
                    self.parent.stacks[stack].y[i].clear()
                for i in self.parent.stacks[stack].x.keys():
                    self.parent.stacks[stack].x[i].clear()
                self.parent.stacks[stack].rechart()
                
            elif stack in ['newEntry',"reviewlast","update"]:
                if stack != "update":
                    self.parent.stacks[stack].model.load_data(currency(),re=True)
                if stack == "update":
                    self.parent.stacks[stack].resultsModel.items.clear()
                    self.parent.stacks[stack].resultsModel.layoutChanged.emit()
        #self.parent.username.setText("")
        #self.parent.password.setText("")

    def lock_action_logout(self,index):
        print(self.parent.stackedWidget.currentIndex(),"logged in"*10)        
        ind=self.parent.stackedWidget.indexOf(self.parent.loggedIn)
        state=self.parent.stackedWidget.currentIndex() == ind

        self.parent.actionLogout.setEnabled(state)
        self.parent.action_Server_Settings.setEnabled(state)
        self.parent.actionUser.setEnabled(state)

    def about_(self):
        self.a=About(self.parent)

    def user_(self):
        self.u=UserDialog(self.parent)
