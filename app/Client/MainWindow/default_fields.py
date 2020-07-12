import json,os,sys,time
from PyQt5.QtWidgets import QHeaderView
from pathlib import Path

def verify():
    return Path("Server/ssl/cert.pem"),Path("Server/ssl/key.pem")


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
def currency_ut():
    return dict(total=0,pennies=0,nickels=0,dimes=0,quarters=0,dollar=0,dollar5=0,dollar10=0,dollar20=0,dollar50=0,dollar100=0)

def currency_ut_plus():
    c=currency_ut()
    c['date']=""
    c['page']=0
    c['limit']=10
    
    c.__delitem__("total")
    
    return c

def currency_lst():
    return dict(total=[],pennies=[],nickels=[],dimes=[],quarters=[],dollar=[],dollar5=[],dollar10=[],dollar20=[],dollar50=[],dollar100=[])
def currency_mx():
    return dict(pennies=0.01,nickels=0.05,dimes=0.1,quarters=0.25,dollar=1,dollar5=5,dollar10=10,dollar20=20,dollar50=50,dollar100=100)

default_password="x"*5

def emails():
    return ['MESSAGING_EMAIL','email','USER_EMAIL_SENDER_EMAIL ']

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
    return {'active': True, 'email': '', 'fname': '', 'id': -1, 'lname': '', 'mname': '', 'password': '', '': '', 'uname': '', 'host': 'http://localhost:9090','phone':'(555) 854-4057','role':"user"}

