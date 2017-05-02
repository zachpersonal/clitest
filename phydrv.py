#!/usr/bin/env python
# -*- coding:utf-8 -*-
#This script is for phydrv command
# initial version by Jacky on April 12th, 2017

import random
from pool import random_key
from email_generator import address_generator
from ssh_connect import ssh_conn
from to_log import tolog
from send_cmd import SendCmd
Pass = "'result': 'p'"
Fail = "'result': 'f'"
Failprompt="Failed on verifying "
from pool import getpdlist

def phydrvlist(c):
    # brief
    # vebose
    pass

def phydrvlocate(c):
    FailFlag=False
    pdlist=getpdlist(c)
    res=[]
    for key in pdlist:
        res.append(SendCmd(c,"phydrv -a locate -p "+ key))
    for eachres in res:
        if "Error" in eachres or "Invalid" in eachres:

            FailFlag = True
            break

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

def getphydrvglobalsettings(c):
    SASsettings = (
    "WriteCache", "RlaCache", "ReadCache", "CmdQueuing", "TempPollInt", "MediumErrorThreshold", "Glatency")
    pdlist = getpdlist(c)

    # get the pdid randomly
    for key in pdlist:
        pdid = key
        break

    result = SendCmd(c, "phydrv -v -p " + pdid)

    #
    # administrator@cli> phydrv -v -p 2
    #
    # Globle Physical Drives Setting for SATA:
    # -------------------------------------------------------------------------------
    # WriteCache: Enabled                     RlaCache: Enabled
    # DmaMode: UDMA6                          CmdQueuing: Enabled
    # TempPollInt: 30                         MediumErrorThreshold: 64
    # Glatency: 0
    #
    # Globle Physical Drives Setting for SAS:
    # -------------------------------------------------------------------------------
    # WriteCache: Enabled                     RlaCache: Enabled
    # ReadCache: Enabled                      CmdQueuing: Enabled
    # TempPollInt: 30                         MediumErrorThreshold: 64
    # Glatency: 60
    SasSettingsdict = {}
    globalphydrvsetting = result.replace("-", "")
    SasSettingsStr = globalphydrvsetting.split("Globle Physical Drives Setting for SAS:")[1].replace(
        "administrator@cli> ", "")
    # import re
    #
    # userslocation = [m.start() for m in re.finditer('Username: ', userdata)]
    for each in SASsettings:
        if each != "MediumErrorThreshold":
            SasSettingsdict[each] = SasSettingsStr[
                                    SasSettingsStr.find(each) + len(each) + 2:SasSettingsStr.find(each) + len(
                                        each) + 11].rstrip()
        else:
            SasSettingsdict[each] = SasSettingsStr[
                                    SasSettingsStr.find(each) + len(each) + 2:SasSettingsStr.find(each) + len(
                                        each) + 4].rstrip()
    return SasSettingsdict

def phydrvmodifyglobalsettings(c):

    Failflag=False
    SasSettingsdict=getphydrvglobalsettings(c)
    NewSasSettingsdict=SasSettingsdict
    settings=""
    for key,value in NewSasSettingsdict.items():
        if SasSettingsdict[key]=="Enabled":
            NewSasSettingsdict[key]="Disabled"
            if settings == "":
                settings = key + "=" + "disable"
            else:

                settings = settings+","+(key + "=" + "disable")
        elif SasSettingsdict[key]=="Disabled":
            NewSasSettingsdict[key]="Enabled"
            if settings=="":

                settings = key + "=" + "enable"
            else:

                settings = settings+","+(key + "=" + "enable")
        if key=="TempPollInt":
            NewSasSettingsdict[key]=str(random.randint(15,255))
            if settings == "":

                settings = key + "=" + NewSasSettingsdict[key]
            else:

                settings = settings+","+(key + "=" + NewSasSettingsdict[key])
        if key=="MediumErrorThreshold":
            NewSasSettingsdict[key] = str(random.randint(1,4294967294))
            if settings == "":

                settings = key + "=" + NewSasSettingsdict[key]
            else:

                settings = settings+","+(key + "=" + NewSasSettingsdict[key])
        # if key=="Glatency":
        #     NewSasSettingsdict[key] = str(random.randint(0,29000))
        #     if settings == "":
        #         settings = key + "=" + NewSasSettingsdict[key]
        #     else:
        #         settings = settings+","+(key + "=" + NewSasSettingsdict[key])

    res=SendCmd(c,"phydrv -a mod -s "+"\""+settings+"\"")

    if "Error" in res or "Invalid" in res:
        Failflag=True

    updatedSasSettings=getphydrvglobalsettings(c)

    diff= dict_diff(NewSasSettingsdict,updatedSasSettings)
    if len(diff['different'])!=0:
        for a in diff['different']:
            tolog(a)
        Failflag = True

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)


def dict_diff(old, new):
    diff = dict()
    diff['old'] = set(old) - set(new)
    diff['new'] = set(new) - set(old)
    diff['different'] = {k for k in set(old) & set(new) if old[k] != new[k]}
    return diff

def phydrvoffline(c):
    Failflag=False
    from pool import poolcreateandlist
    from pool import poolforceclean
    from pool import sparedrvcreate
    from pool import getpdlist
    import time
    poolforceclean(c)
    poolcreateandlist(c,1)
    sparedrvcreate(c,1)
    spareid=SendCmd(c,"spare -v").split("PdId: ")[1][0:2].strip()
    # get pdids that are for pool0
    # method 1
    # pddict=getpdlist(c)
    # pool0pds=[]
    # for key,value in pddict.items():
    #     if "Pool0" in value:
    #         pool0pds.append(key)

    #method 2
    res=SendCmd(c,"pool -v -i 0")
    pool0pds=res.split("Pds: ")[1].replace("administrator@cli> ","").strip()

    # send offline cmd
    SendCmd(c,"phydrv -a offline -p "+pool0pds[0])

    # verify spare drive is rebuilding
    resbuilding=SendCmd(c,"phydrv")
    if "Rebuilding" in resbuilding:
        tolog("spare drive %s is rebuilding." %spareid)
    else:
        tolog("Rebuilding does not work on spare drive %s" %spareid)
        Failflag =True
    i=0
    while "Rebuilding" in resbuilding and i< 30:
        tolog("Rebuilding is ongoing, elasped %s" %str(i))

        resbuilding=SendCmd(c, "phydrv")
        time.sleep(1)
        i+=1
        if i==30:
            tolog("Because rebuilding process will take too much time, the script will not record the process any more.")
    # else:
    #     tolog("Rebuilding is done.")
    # verify the original spare drive is in pool0
    res = SendCmd(c, "pool -v -i 0")
    updated_pool0pds = res.split("Pds: ")[1].replace("administrator@cli> ", "").strip()
    if spareid in updated_pool0pds:
        tolog("spare drive %s is in pool0" % spareid)
    else:
        tolog("NOTE: spare drive %s is not in pool0" % spareid)
        Failflag = True
    # verify the offlined drive is Stale, Staleconfig status
    pddict = getpdlist(c)
    for key, value in pddict.items():
        if "Stale" in value:
            stalepdid = key
            break

    if key == pool0pds[0]:
        tolog("drive %s is stale" % pool0pds[0])
    else:
        tolog("NOTE: drive %s is not stale" % pool0pds[0])
        Failflag = True

    SendCmd(c, "phydrv -a clear -t staleconfig -p " + pool0pds[0])

    updated_pddict = getpdlist(c)
    staleflag=False
    for key, value in updated_pddict.items():
        if "Stale" in value:
            tolog("Clear Staleconfig failed")
            staleflag=True
            Failflag = True
    if not staleflag:
        tolog("Clear Staleconfig successfully.")

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)


if __name__ == "__main__":

    import time
    start = time.clock()
    start2=time.time()
    c, ssh = ssh_conn()
    SendCmd(c,"about")

    # get physical global settings
    # modify these settings
    # verify the modified settings
    #phydrvmodifyglobalsettings(c)

    #phydrvoffline(c)

    ssh.close()
    elasped1 = time.clock() - start
    elasped2 = time.time()-start2
    print "Elasped1 %s" % elasped1
    print "Elasped2 %s" % elasped2