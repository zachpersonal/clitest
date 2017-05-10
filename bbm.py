# coding=utf-8
# initial sample work on 2016.12.23
# this section includes verify proper cmd/parameters/options and
# some other boundary or misspelled parameters/options
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
import random

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyBBM(c):
    FailFlag = False

    # find configured PdId in phydrv list
    def findPdId():
        result = SendCmd(c, "phydrv")
        num = 4
        pdid = []
        while result.split("\r\n")[num] != 'administrator@cli> ':
            row = result.split("\r\n")[num]
            configStatusIsPool = ''
            if not row.split()[9].isalpha():
                configStatusIsPool = row.split()[9][:-1]
            if row.split()[9] in "WriteCache ReadCache Global Dedicated" or configStatusIsPool == "Pool":
                pdid.append(row.split()[0])
            num = num + 1
        return pdid

    tolog("Verify bbm")
    # find configured PdId in bbm list and verify bbm
    pdid = findPdId()
    result = SendCmd(c, "bbm")
    num = 2
    bbmpdid = []
    while result.split("\r\n")[num] != 'administrator@cli> ':
        print result.split("\r\n")[num]
        if "Drive Id:" in result.split("\r\n")[num]:
           bbmpdid.append(result.split("\r\n")[num].split()[-1])
        num = num + 1
    if pdid != bbmpdid:
        FailFlag = True
        tolog("Fail: Verify bbm")

    tolog("Verify bbm -p PD's ID that the configstatus is configured")
    pdid = findPdId()
    for m in pdid:
        result = SendCmd(c, "bbm -p " + m)
        if "Error" in result or "Drive Id: " +m not in result:
            FailFlag = True
            tolog("Fail: bbm -p " + m)

    tolog("Verify bbm -v -p PD's ID that the configstatus is configured")
    pdid = findPdId()
    for m in pdid:
        result = SendCmd(c, "bbm -v -p " + m)
        if "Error" in result or "Drive Id: " +m not in result:
            FailFlag = True
            tolog("Fail: bbm -v -p " + m)

    tolog("Verify bbm -p PD's ID that the configstatus is Unconfigured")
    result = SendCmd(c, "phydrv")
    num = 4
    pdid = []
    while result.split("\r\n")[num] != 'administrator@cli> ':
        row = result.split("\r\n")[num]
        if row.split()[-1] == "Unconfigured":
            pdid.append(row.split()[0])
        num = num + 1
    Rpdid = random.choice(pdid)
    result = SendCmd(c, "bbm -p " + Rpdid)
    if "Error" not in result:
        FailFlag = True
        tolog("Fail: bbm -p " + Rpdid)

    tolog("Verify bbm -p PD's ID that the configstatus is Unconfigured -v")
    result = SendCmd(c, "phydrv")
    num = 4
    pdid = []
    while result.split("\r\n")[num] != 'administrator@cli> ':
        row = result.split("\r\n")[num]
        if row.split()[-1] == "Unconfigured":
           pdid.append(row.split()[0])
        num = num + 1
    Rpdid = random.choice(pdid)
    result = SendCmd(c, "bbm -p " + Rpdid + " -v")
    if "Error" not in result:
        FailFlag = True
        tolog("Fail: bbm -p " + Rpdid + " -v")

    tolog("Verify bbm -p there is no pd's id")
    result = SendCmd(c, "bbm -p 500")
    if "Error" not in result:
        FailFlag = True
        tolog("Fail: Verify bbm -p 500")

    tolog("Verify bbm -p there is no pd's id -v")
    result = SendCmd(c, "bbm -p 1024 -v")
    if "Error" not in result:
        FailFlag = True
        tolog("Fail: Verify bbm -p -v 500")

    tolog("Verify bbm -p x")
    result = SendCmd(c, "bbm -p x")
    if "Error" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail: Verify bbm -p x")

    tolog("Verify bbm -p -x")
    result = SendCmd(c, "bbm -p -x")
    if "Error" not in result or "Invalid option" not in result:
        FailFlag = True
        tolog("Fail: Verify bbm -p -x")

    if FailFlag:
        tolog('Fail: Verify bbm')
        tolog(Fail)
    else:
        tolog('Pass')
        tolog(Pass)

def verifybbmlist(c):
    FailFlag = False

    # find configured PdId in phydrv list
    def findPdId():
        result = SendCmd(c, "phydrv")
        num = 4
        pdid = []
        while result.split("\r\n")[num] != 'administrator@cli> ':
            row = result.split("\r\n")[num]
            configStatusIsPool = ''
            if not row.split()[9].isalpha():
                configStatusIsPool = row.split()[9][:-1]
            if row.split()[9] in "WriteCache ReadCache Global Dedicated" or configStatusIsPool == "Pool":
                pdid.append(row.split()[0])
            num = num + 1
        return pdid

    tolog("Verify bbm -a list")
    # find configured PdId in bbm list and verify bbm
    pdid = findPdId()
    result = SendCmd(c, "bbm -a list")
    num = 2
    bbmpdid = []
    while result.split("\r\n")[num] != 'administrator@cli> ':
        print result.split("\r\n")[num]
        if "Drive Id:" in result.split("\r\n")[num]:
           bbmpdid.append(result.split("\r\n")[num].split()[-1])
        num = num + 1
    if pdid != bbmpdid:
        FailFlag = True
        tolog("Fail: Verify bbm -a list")

    tolog("Verify bbm -a list -p PD's ID that the configstatus is configured")
    pdid = findPdId()
    for m in pdid:
        result = SendCmd(c, "bbm -a list -p " + m)
        if "Error" in result or "Drive Id: " + m not in result:
            FailFlag = True
            tolog("Fail: bbm -a list -p " + m)

    tolog("Verify bbm -a list -v -p PD's ID that the configstatus is configured")
    pdid = findPdId()
    for m in pdid:
        result = SendCmd(c, "bbm -a list -v -p " + m)
        if "Error" in result or "Drive Id: " +m not in result:
            FailFlag = True
            tolog("Fail: bbm -a list -v -p " + m)

    tolog("Verify bbm -a list -p PD's ID that the configstatus is Unconfigured")
    result = SendCmd(c, "phydrv")
    num = 4
    pdid = []
    while result.split("\r\n")[num] != 'administrator@cli> ':
        row = result.split("\r\n")[num]
        if row.split()[-1] == "Unconfigured":
           pdid.append(row.split()[0])
        num = num + 1
    Rpdid = random.choice(pdid)
    result = SendCmd(c, "bbm -a list -p " + Rpdid)
    if "Error" not in result:
        FailFlag = True
        tolog("Fail: bbm -a list -p " + Rpdid)

    tolog("Verify bbm -a list -p PD's ID that the configstatus is Unconfigured -v")
    result = SendCmd(c, "phydrv")
    num = 4
    pdid = []
    while result.split("\r\n")[num] != 'administrator@cli> ':
        row = result.split("\r\n")[num]
        if row.split()[-1] == "Unconfigured":
           pdid.append(row.split()[0])
        num = num + 1
    Rpdid = random.choice(pdid)
    result = SendCmd(c, "bbm -a list -p " + Rpdid + " -v")
    if "Error" not in result:
        FailFlag = True
        tolog("Fail: bbm -a list -p " + Rpdid + " -v")

    tolog("Verify bbm -a list -p there is no pd's id")
    result = SendCmd(c, "bbm -a list -p 500")
    if "Error" not in result:
        FailFlag = True
        tolog("Fail: Verify bbm -a list -p 500")

    tolog("Verify bbm -a list -p there is no pd's id -v")
    result = SendCmd(c, "bbm -a list -a list -p 1024 -v")
    if "Error" not in result:
        FailFlag = True
        tolog("Fail: Verify bbm -a list -p -v 500")

    tolog("Verify bbm -a list -p x")
    result = SendCmd(c, "bbm -a list -p x")
    if "Error" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail: Verify bbm -a list -p x")

    tolog("Verify bbm -a list -p -x")
    result = SendCmd(c, "bbm -a list -p -x")
    if "Error" not in result or "Invalid option" not in result:
        FailFlag = True
        tolog("Fail: Verify bbm -a list -p -x")

    if FailFlag:
        tolog('Fail: Verify bbm -a list')
        tolog(Fail)
    else:
        tolog('Pass')
        tolog(Pass)

def verifybbmclear(c):
    FailFlag = False

    tolog("Verify bbm -a clear -p pd's ID (configured SATA physical drive)")
    result = SendCmd(c, "phydrv")
    num = 4
    pdid = []
    while result.split("\r\n")[num] != 'administrator@cli> ':
        row = result.split("\r\n")[num]
        if row.split()[2] != "SAST":
            FailFlag = True
            tolog("Fail: bbm -a clear -p pd's ID (configured SATA physical drive) because there is no SAST type PD")
            break
        if row.split()[2] == "SAST" and row.split()[-1] != "Unconfigured":
            pdid.append(row.split()[0])
        num = num + 1
    if len(pdid) != 0:
        for m in pdid:
            result = SendCmd(c, "bbm -a clear " + m)
            if "Error" in result:
                FailFlag = True
                tolog("Fail: Verify bbm -a clear " + m)

    tolog("Verify bbm -a clear -p pd's id (unconfigured SATA physical drive)")
    result = SendCmd(c, "phydrv")
    num = 4
    pdid = []
    while result.split("\r\n")[num] != 'administrator@cli> ':
        row = result.split("\r\n")[num]
        if row.split()[2] != "SAST":
            FailFlag = True
            tolog("Fail: bbm -a clear -p pd's id (unconfigured SATA physical drive), because there is no SAST type PD")
            break
        if row.split()[2] == "SAST" and row.split()[-1] == "Unconfigured":
            pdid.append(row.split()[0])
        num = num + 1
    if len(pdid) != 0:
        for m in pdid:
            result = SendCmd(c, "bbm -a clear " + m)
            if "Error" in result:
                FailFlag = True
                tolog("Fail: Verify bbm -a clear " + m)

    tolog("Verify bbm -a clear -p pd's id(configured not SATA physical drive)")
    result = SendCmd(c, "phydrv")
    num = 4
    pdid = []
    while result.split("\r\n")[num] != 'administrator@cli> ':
        row = result.split("\r\n")[num]
        if row.split()[2] != "SAST" and row.split()[-1] != "Unconfigured":
            pdid.append(row.split()[0])
        num = num + 1
    Rpdid = random.choice(pdid)
    result = SendCmd(c, "bbm -a clear -p " + Rpdid)
    if "Error" not in result:
        FailFlag =True
        tolog("Fail: bbm -a clear -p " + Rpdid)

    tolog("Verify bbm -a clear -p pd's id(Unconfigured not SATA physical drive)")
    result = SendCmd(c, "phydrv")
    num = 4
    pdid = []
    while result.split("\r\n")[num] != 'administrator@cli> ':
        row = result.split("\r\n")[num]
        if row.split()[2] != "SAST" and row.split()[-1] == "Unconfigured":
            pdid.append(row.split()[0])
        num = num + 1
    Rpdid = random.choice(pdid)
    result = SendCmd(c, "bbm -a clear -p " + Rpdid)
    if "Error" not in result:
        FailFlag =True
        tolog("Fail: bbm -a clear -p " + Rpdid)

    tolog("Verify bbm -a clear -p pd's ID")
    result = SendCmd(c, "bbm -a clear -p 1")
    if "Error" not in result:
        FailFlag = True
        tolog("Fail: bbm -a clear -p pd's ID")

    tolog("Verify bbm -a clear -x")
    result = SendCmd(c, "bbm -a clear -x")
    if "Error" not in result:
        FailFlag = True
        tolog("Fail: bbm -a clear -x")

    if FailFlag:
        tolog('Fail: Verify bbm -a clear')
        tolog(Fail)
    else:

        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyBBM(c)
    verifybbmlist(c)
    verifybbmclear(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped