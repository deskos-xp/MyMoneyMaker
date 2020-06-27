import json,os,sys
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
        pennies=None,
        nickels=None,
        dimes=None,
        quarters=None,
        dollar=None,
        dollar5=None,
        dollar10=None,
        dollar20=None,
        dollar50=None,
        dollar100=None,
        id=None,
        date=""
    )
