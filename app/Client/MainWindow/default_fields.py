import json,os,sys,time
from PyQt5.QtWidgets import QHeaderView
def prep_table(table):
    table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
def help_():
    return dict(
            name="",
            version="",
            author="",
            email="",
            comment=""
            )

def currency():
    return dict(
        pennies=0,
        nickels=0,
        dimes=0,
        quarters=0,
        dollar=0,
        dollar5=0,
        dollar10=0,
        dollar20=0,
        dollar50=0,
        dollar100=0,
        id=0,
        date=time.strftime("%m/%d/%Y",time.localtime())
    )
def user():
    return {'active': True, 'email': '', 'fname': '', 'id': -1, 'lname': '', 'mname': '', 'password': '', '': '', 'roles': [], 'uname': '', 'host': 'http://localhost:9090'}

