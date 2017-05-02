#!/usr/bin/env python
# -*- coding:utf-8 -*-
#This script is for user command
# initial version from Hulda
# modified by Jacky on April 6th, 2017


# def ListUserinfo():
#     tolog("===Getting user list!===")
#     FailFlag = Fail
#     if "Error" in SendCmd("user"):
#         print "user command has error!"
#         tolog("user command has error!")
#         FailFlag = True
#     else:
#         userlist = SendCmd("user").split("\r\n")[4:-2]
#         print "list====", userlist
#         Username = [value.split()[0] for value in userlist]
#         print "Username:===", Username
#     return Username
#
# def Product_username():
#     username = ""
#     a = "abcdefghigklmnopqrstuvwxyz0123456789_"
#     n = random.randint(1,31)
#     for i in range(1,n+1):
#         username += random.choice(a)
#     #print "username is ===",username
#     return username
#
# def AddMgmtuser():
#
#     FailFlag = Fail
#     username = Product_username()
#     privilege = random.choice(["super","power","maintenance","view"])
#     status = random.choice(["enable","disable"])
#     email = username+"@"+ "user.com"
#     result = SendCmd('user -a add -t mgmt -u %s -p %s -s "status=%s,name=%s,email=%s"' % (username,privilege,status,username,email))
#     #print result


class User:
    def usercreate(self):
        pass
    def userlist(self):
        pass
    def usermodify(self):
        pass
    def userdelete(self):
        pass

import random
from pool import random_key
from email_generator import address_generator
from ssh_connect import ssh_conn
from to_log import tolog
from send_cmd import SendCmd

Pass = "'result': 'p'"
Fail = "'result': 'f'"
Failprompt="Failed on verifying "

def usercreate(c,usertype,privilegetype):

    username=random_key(31)
    displayname = random_key(31)
    department=random_key(31)
    phone=random_key(31)
    emailaddress=address_generator()
    privilege=("Super","Power","Maintenance","View")
    type= ("mgmt","snmp","ds")
    auth= ("md5","sha")
    priv=("des", "aes")

    # test 1
    # user type: mgmt
    if usertype=="mgmt":
        if privilegetype!="":

            userinfo = {"username": username, "displayname": displayname, "emailaddress": emailaddress,
                        "privilege": privilegetype}
        else:
            userinfo = {"username": username, "displayname": displayname, "emailaddress": emailaddress,
                        "privilege": random.choice(privilege)}
        settings = " -u " + userinfo["username"] + " -p " + userinfo[
                "privilege"] + " -t " + usertype + " -s " + "\"name=" + userinfo["displayname"] + ",email=" + userinfo[
                           "emailaddress"] + "\""
            # print settings
        # create users
        SendCmd(c, "user -a add " + settings)
        # verify the created users
        userverify(c, userinfo)
        # modify the status and name of the above users
        # and verify the modified users
        usermodify(c,userinfo["username"])
    # test 2
    # user type: snmp
    if usertype=="snmp":
        pass

    # test 2
    # user type: snmp
    if usertype=="ds":
        pass

def userverify(c,userinfo):
    FailFlag = False
    briefoutput=(SendCmd(c,"user"),SendCmd(c,"user -a list"),SendCmd(c,"user -a list -u "+userinfo["username"]))

    for op in briefoutput:
        for key,value in userinfo.items():
            if value[:10] not in op:
                tolog("%s created unsucessfully beause %s is not in the list" % userinfo["username"] % value[:10])
                FailFlag = True
                break


    verboseoutput=(SendCmd(c,"user -v"),SendCmd(c,"user -v -a list"),SendCmd(c,"user -v -u "+userinfo["username"]))

    for op in verboseoutput:
        for key,value in userinfo.items():
            if value not in op:
                tolog("%s created unsucessfully beause %s is not in the list" % userinfo["username"] % value)
                FailFlag = True
                break

    if FailFlag:
        tolog(Fail)
    else:
        tolog("User is created successully.")
        tolog(Pass)

def userdelete(c):
    users=usergetinfo(c)
    print users
    for user in users:
        SendCmd(c,"user -a del -u "+user)

def usergetinfo(c):

    import re
    userdata=SendCmd(c,"user -v")
    userslocation=[m.start() for m in re.finditer('Username: ', userdata)]
    usersstatus=[m.start() for m in re.finditer('Status: ', userdata)]
    userslist=list()
    i = 0
    for userlocation in userslocation:
        print userdata[userlocation+10:usersstatus[i]-1]
        userslist.append((userdata[userlocation+10:usersstatus[i]-1]).rstrip())
        i+=1
    return userslist



def usermodify(c,username):

    # only status and display name are to be modified.

    Failflag=False
    newdisplayname=random_key(31)

    userdata=SendCmd(c,"user -u "+username)
    if "Enabled" in userdata:

        SendCmd(c,"user -a mod -u "+username+" -s "+"\"status=disable,name="+newdisplayname+"\"")
        res=SendCmd(c,"user -v -u "+username)
        if "Disabled" in res and newdisplayname in res:
            tolog("Modified user %s info successfully." %username)
        else:
            Failflag=True
            tolog("Modified user %s info failed." % username)

    else:
        SendCmd(c, "user -a mod -u " + username + " -s " + "\"status=enable,name=" + newdisplayname + "\"")
        res = SendCmd(c, "user -v -u " + username)
        if "Enabled" in res and newdisplayname in res:
            tolog("Modified user %s info successfully." % username)
        else:
            Failflag = True
            tolog("Modified user %s info failed." % username)

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

# def usermodifiedverify(c,status,name):
#
#     Failflag=False
#     res=SendCmd(c,"user -u "+ name)
#     if status in res:
#         tolog("The %s is %s." %name %status)
#
#     else:
#         a="changed name %s or its status %s." %name %status
#         tolog(Failprompt+a)
#         Failflag=True
#
#     if Failflag:
#         return True
#     else:
#         return False



if __name__ == "__main__":

    import time
    start = time.clock()
    start2 = time.time()
    c, ssh = ssh_conn()
    SendCmd(c,"about")
    # test case 1: mgmt
    userdelete(c)

    # create 15 users and modify the status and display name
    for i in range(3):
         usercreate(c,"mgmt","")

    ssh.close()
    elasped = time.clock() - start
    elasped2 = time.time() - start2
    print "Elasped %s" % elasped
    print "Elasped2 %s" % elasped2