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

def verifySmart(c):
    FailFlag = False

    # find configured PdId in phydrv list
    def findPdId():
        result = SendCmd(c, "phydrv")
        num = 4
        PdId = []
        while result.split("\r\n")[num] != 'administrator@cli> ':
            row = result.split("\r\n")[num]
            PdId.append(row.split()[0])
            num = num + 1
        return PdId

    tolog("Verify smart")
    PdId = findPdId()
    result = SendCmd(c, "smart")
    num = 4
    smartPdId = []
    while result.split("\r\n")[num] != 'administrator@cli> ':
        row = result.split("\r\n")[num]
        smartPdId.append(row.split()[0])
        num = num + 1
    if smartPdId != PdId:
        FailFlag = True
        tolog("Fail: smart")

    tolog("Verify smart -p ")
    PdId = findPdId()
    for m in PdId:
        result = SendCmd(c, "smart -p " + m)
        row = result.split("\r\n")
        if row[2] not in result or row[4].split()[0] != m:
            FailFlag = True
            tolog("Fail: smart -p " + m)

    tolog("Verify smart -p number(no pd's id, 1~512)")
    PdId = findPdId()
    print PdId[-1]
    if (int(PdId[-1]) + 1) <= 512:
        result = SendCmd(c, "smart -p " + str(int(PdId[-1]) + 1))
        if "Error" not in result or "Physical drive not found" not in result:
            FailFlag = True
            tolog("Fail: smart -p number(no pd's id, 1~512)")
    else:
        tolog("Fail: smart -p number(no pd's id, 1~512), because slot is full.")

    tolog("Verify smart -p number(<1 or >512)")
    for m in [-1, 0, 513]:
        result = SendCmd(c, "smart -p " + str(m))
        if "Error" not in result:
            FailFlag = True
            tolog("Fail: smart -p number(<1 or >512)")

    tolog("Verify smart -p a")
    result = SendCmd(c, "smart -p a")
    if "Error" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail: smart -p a")

    tolog("Verify smart x")
    result = SendCmd(c, "smart x")
    if "Error" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail: smart x")

    tolog("Verify smart -x")
    result = SendCmd(c, "smart -x")
    if "Error" not in result or "Invalid option" not in result:
        FailFlag = True
        tolog("Fail: smart -x")

    if FailFlag:
        tolog('Fail: Verify bbm')
        tolog(Fail)
    else:
        tolog('Pass')
        tolog(Pass)

def verifySmartV(c):
    FailFlag = False

    # find configured PdId in phydrv list
    def findPdId():
        result = SendCmd(c, "phydrv")
        num = 4
        PdId = []
        while result.split("\r\n")[num] != 'administrator@cli> ':
            row = result.split("\r\n")[num]
            PdId.append(row.split()[0])
            num = num + 1
        return PdId

    tolog("Verify smart -v")
    result = SendCmd(c, "smart -v")
    if "Error (" in result:
        FailFlag = True
        tolog("Fail: smart -v")

    tolog("Verify smart -v -p ")
    result = SendCmd(c, "smart")
    enablePdId = []
    disablePdId = []
    num = 4
    while result.split("\r\n")[num] != 'administrator@cli> ':
        row = result.split("\r\n")[num]
        if row.split()[-1] == "Disabled":
            disablePdId.append(row.split()[0])
        if row.split()[-1] == "Enabled":
            enablePdId.append(row.split()[0])
        num = num + 1
    # When PD smart is enable, verify smart -v -p
    if len(enablePdId) != 0:
        for m in enablePdId:
            result = SendCmd(c, "smart -v -p " + m)
            PDModel = (SendCmd(c, "phydrv -p " + m).split("\r\n")[4]).split()[1]
            smartPDModel = result.split("\r\n")[3].split()[-1]
            if result.split("\r\n")[2] != "PdId: " + m or PDModel != smartPDModel or "SMART Health Status: OK" not in result:
                FailFlag = True
                tolog("Fail: smart -v -p " + m)
    # When PD smart is disable, verify smart -v -p
    if len(disablePdId) != 0:
        for m in disablePdId:
            result = SendCmd(c, "smart -p " + m + " -v")
            PDModel = (SendCmd(c, "phydrv -p " + m).split("\r\n")[4]).split()[1]
            smartPDModel = result.split("\r\n")[3].split()[-1]
            if result.split("\r\n")[2] != "PdId: " + m or PDModel != smartPDModel:
                FailFlag = True
                tolog("Fail: smart -p " + m + " -v")

    tolog("Verify smart -v -p number(no pd's id, 1~512)")
    PdId = findPdId()
    print PdId[-1]
    if (int(PdId[-1]) + 1) <= 512:
        result = SendCmd(c, "smart -v -p " + str(int(PdId[-1]) + 1))
        if "Error" not in result or "Physical drive not found" not in result:
            FailFlag = True
            tolog("Fail: smart -v -p " + str(int(PdId[-1]) + 1))
    else:
        tolog("Fail: smart -v -p number(no pd's id, 1~512), because slot is full.")

    tolog("Verify smart -v -p number(<1 or >512)")
    for m in [-1, 0, 513]:
        result = SendCmd(c, "smart -v -p " + str(m))
        if "Error" not in result:
            FailFlag = True
            tolog("Fail: smart -v -p " + str(m))

    tolog("Verify smart -v -p a")
    result = SendCmd(c, "smart -v -p a")
    if "Error" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail: smart -v -p a")

    tolog("Verify smart -v x")
    result = SendCmd(c, "smart -v x")
    if "Error" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail: smart -v x")

    tolog("Verify smart -v -x")
    result = SendCmd(c, "smart -v -x")
    if "Error" not in result or "Invalid option" not in result:
        FailFlag = True
        tolog("Fail: smart -v -x")

    if FailFlag:
        tolog('Fail: Verify bbm -v')
        tolog(Fail)
    else:
        tolog('Pass')
        tolog(Pass)

def verifyList(c):
    FailFlag = False
    def findPdId():
        result = SendCmd(c, "phydrv")
        num = 4
        PdId = []
        while result.split("\r\n")[num] != 'administrator@cli> ':
            row = result.split("\r\n")[num]
            PdId.append(row.split()[0])
            num = num + 1
        return PdId

    tolog("Verify smart -a list")
    result = SendCmd(c, "smart -a list")
    if "Error (" in result:
        FailFlag = True
        tolog("Fail: smart -a list")

    tolog("Verify smart -a list -v")
    result = SendCmd(c, "smart -a list -v")
    if "Error (" in result:
        FailFlag = True
        tolog("Fail: smart -a list -v")

    tolog("Verify smart -a list -p pd's id")
    PdId = findPdId()
    result = SendCmd(c, "smart -a list -p " + random.choice(PdId))
    if "Error (" in result:
        FailFlag = True
        tolog("Fail: smart -a list -p " + random.choice(PdId))

    tolog("Verify smart -a list -v -p pd's id")
    PdId = findPdId()
    result = SendCmd(c, "smart -a list -v -p " + random.choice(PdId))
    if "Error (" in result:
        FailFlag = True
        tolog("Fail: smart -a list -v -p " + random.choice(PdId))

    tolog("Verify smart -a list -v -p there is no pd's ID")
    PdId = findPdId()
    result = SendCmd(c, "smart -a list -v -p " + str(int(PdId[-1]) + 1))
    if "Error (" not in result or "Invalid parameter" not in result:
        FailFlag = True
        tolog("Fail: smart -a list -v -p " + str(int(PdId[-1]) + 1))

    tolog("Verify smart -a list -v -p x")
    result = SendCmd(c, "smart -a list -v -p x")
    if "Error (" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail smart -a list -v -p x")

    tolog("Verify smart -a list -v -x")
    result = SendCmd(c, "smart -a list -v -x")
    if "Error (" not in result or "Invalid option" not in result:
        FailFlag = True
        tolog("Fail smart -a list -v -p x")

    tolog("Verify smart -a abc")
    result = SendCmd(c, "smart -a abc")
    if "Error (" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail smart -a abc")

    if FailFlag:
        tolog('Fail: Verify bbm -a list -v')
        tolog(Fail)
    else:
        tolog('Pass')
        tolog(Pass)

def verifyEnableAndDisable(c):
    FailFlag = False
    def findPdId():
        result = SendCmd(c, "phydrv")
        num = 4
        PdId = []
        while result.split("\r\n")[num] != 'administrator@cli> ':
            row = result.split("\r\n")[num]
            PdId.append(row.split()[0])
            num = num + 1
        return PdId
    tolog("Verify smart -a [enable,disable] -p pd's ID")
    PdId = random.choice(findPdId())
    for values in ['enable ', 'disable ', 'disable ', 'enable ', 'enable ']:
        result = SendCmd(c, "smart -a " + values + "-p " + PdId)
        if "Error (" in result:
            FailFlag = True
            tolog("Fail: smart -a " + values + "-p " + PdId)

    tolog("Verify smart -a [enable,disable] -p there is no pd's ID")
    for values in ['enable ', 'disable ']:
        result = SendCmd(c, "smart -a " + values + "-p " + str(int(findPdId()[-1]) + 1))
        if "Error (" not in result or "Invalid parameter" not in result:
            FailFlag = True
            tolog("Fail smart -a " + values + "-p " + str(int(findPdId()[-1]) + 1))

    tolog("Verify smart -a [enable,disable] -p x")
    for values in ['enable ', 'disable ']:
        result = SendCmd(c, "smart -a " + values + "-p x")
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog("Fail smart -a " + values + "-p x")

    tolog("Verify smart -a [enable,disable] pd's ID")
    PdId = random.choice(findPdId())
    for values in ['enable ', 'disable ']:
        result = SendCmd(c, "smart -a " + values + PdId)
        if "Error ("  not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog("Fail: smart -a " + values + PdId)

    if FailFlag:
        tolog('Fail: Verify bbm -a list -v')
        tolog(Fail)
    else:
        tolog('Pass')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifySmart(c)
    verifySmartV(c)
    verifyList(c)
    verifyEnableAndDisable(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped