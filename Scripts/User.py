#!/usr/bin/env python
# -*- coding:utf-8 -*-
#This script is for user command

from ssh_cmd import SendCmd
from ssh_connect import ssh_conn
from to_log import tolog
import random

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def ListUserinfo():
    tolog("===Getting user list!===")
    FailFlag = Fail
    if "Error" in SendCmd("user"):
        print "user command has error!"
        tolog("user command has error!")
        FailFlag = True
    else:
        userlist = SendCmd("user").split("\r\n")[4:-2]
        print "list====", userlist
        Username = [value.split()[0] for value in userlist]
        print "Username:===", Username
    return Username

def Product_username():
    username = ""
    a = "abcdefghigklmnopqrstuvwxyz0123456789_"
    n = random.randint(1,31)
    for i in range(1,n+1):
        username += random.choice(a)
    #print "username is ===",username
    return username

def AddMgmtuser():

    FailFlag = Fail
    username = Product_username()
    privilege = random.choice(["super","power","maintenance","view"])
    status = random.choice(["enable","disable"])
    email = username+"@"+ "user.com"
    result = SendCmd('user -a add -t mgmt -u %s -p %s -s "status=%s,name=%s,email=%s"' % (username,privilege,status,username,email))
    #print result







if __name__ == "__main__":
    #ListUserinfo()
    #Product_username()
    AddMgmtuser()