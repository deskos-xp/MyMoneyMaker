import argparse
import json,os,sys


class parser:
    def __init__(self):
        self.parser=argparse.ArgumentParser()
        self.cmd=self.parser.add_subparsers(dest="cmd")
        '''
        self.other_sql_server=self.cmd.add_parser("other-sql-server",help="use a different MySQL server")
        self.other_sql_server.add_argument("-a","--host",help="sql server address",default="localhost")
        self.other_sql_server.add_argument("-p","--port",help="sql server port",default=3306)
        self.other_sql_server.add_argument("-u","--username",help="username to log into the server with",default="admin")
        self.other_sql_server.add_argument("-P","--password",help="password to log into the SQL server with",default="avalon")
        '''
        '''
        self.other_flask=self.cmd.add_parser("other-flask",help="use a different flask server")
        self.other_flask.add_argument("-a","--host",help="URI for flask server",default="http://localhost:9090")
        self.other_flask.add_argument("-u","--user",help="user for flask server",default="admin")
        self.other_flask.add_argument("-p","--password",help="password for flask server",default="avalon")
        self.other_flask.add_argument("-P","--port",help="port for flask server",default=9090)
        self.other_flask.add_argument("-pro","--protocol",default="http",help="protocol to used on host")
        '''
        self.adjust_flask=self.cmd.add_parser("adjust-flask",help="modify flask settings from cmd")
        self.adjust_flask.add_argument("-P","--port",help="port for flask server",default=9090)
        self.adjust_flask.add_argument("-pro","--protocol",default="http",help="protocol to used on host")




        self.parser.add_argument("-nf","--no-flask",help="start the client without the flask server",action="store_true")

        self.options=self.parser.parse_args()

if __name__ == "__main__":
    p=parser()
    print(p.options)
