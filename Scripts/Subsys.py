# coding=utf-8
# initial work on 2016.12.28
# this section includes verify proper cmd/parameters/options and
# some other boundary or misspelled parameters/options
from  send_cmd import SendCmd
from to_log import tolog
import string
import json

# define the test result for testlink api
Pass = "'result': 'p'"
Fail = "'result': 'f'"
Failprompt="Failed on verifying "


def getSubsysVinfo(c):
    result = ""
    tolog("Get Subsystem model name:")
    result = SendCmd(c, "subsys -v")
    modelNameValue = (result.split("\\n")[1]).replace("Vendor: Promise Technology,Inc.        Model: ", "")
    return modelNameValue


def verifySubsysInfo(c):
    result = ""
    FailFlag = False
    tolog("Verify subsys info:")
    result = SendCmd(c, "subsys -v"), SendCmd(c, "subsys")
    for each in result:
        if 'Error' in each:
            FailFlag = True
            tolog(Failprompt+each)

    if FailFlag:
        tolog('Verify subsys info fail')
        tolog(Fail)
    else:
        tolog('Verify subsys info pass')
        tolog(Pass)


def modifyAndVerifyAliasSetting(c):
    # only letters, blank space and underscore are accepted
    # other chars are verified
    # no more than 48 char
    # leading spaces and tailing spaces are removed in the alias
    # length subsys alias = 48 chars
    # length controller alias = 48 chars
    # length array,ld alias =32 cahrs
    result = ""
    FailFlag = False
    stdName = "T st_123"
    norm_params = ["alias=" + stdName, "alias=" + stdName * 6, "alias=Test123", "alias=Test",
                   "alias=12345678", "alias=__________", "alias=           ", "alias=Ted Test", "alias=  Ted Test",
                   "alias=Ted Test   ", "alias=__Ted Test"]
    #abnorm_params = ["alias=" + stdName * 7 + "1234567", "alias=" + " " * 60, "alias=Test@123", "alias=#Test",
    #                 "alias=12345678%", "alias=" + "12345678" * 8, "alias=" + "_" * 60 + "", "alias=中文"]
    abnorm_params = ["alias=" + stdName * 7 + "1234567", "alias=Test@123", "alias=#Test",
                     "alias=12345678%", "alias=" + "12345678" * 8, "alias=" + "_" * 60 + ""]
    for each in norm_params:
        tolog("Modify subsys settings by " + "subsys -a mod -s \"" + each + "\"")
        aliasName = string.replace(each, "alias=", "")
        result = SendCmd(c, "subsys -a mod -s \"" + each + "\"")
        checkresult = SendCmd(c, "subsys -v")
        if not ("Error" not in result and (aliasName.lstrip()).rstrip() in checkresult):
            tolog("Failed on verifying " + aliasName)
            FailFlag = True
            tolog(Failprompt+each)

    for each in abnorm_params:
        tolog("Modify subsys alias by " + "subsys -a mod -s \"" + each + "\"")
        aliasName = string.replace(each, "alias=", "")
        result = SendCmd(c, "subsys -a mod -s \"" + each + "\"")
        checkresult = SendCmd(c, "subsys -v")
        if not ("Error" in result and (
                            'alias must contain only alphanumeric characters, blank spaces and underscores' in checkresult or "alias must be no longer than 48 characters" in result or 'Invalid character in alias' in result)):
            # subsys -a mod -s "alias=local#123"
            # -s: alias must contain only alphanumeric characters, blank spaces and underscores
            # Error (0x2034): Invalid character in alias

            # subsys -a mod -s "alias=111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
            # -s: alias must be no longer than 48 characters
            # Error (0x2014): Setting parameters too long

            # subsys - a mod - s "alias=12345678%"
            # -s: alias must contain only alphanumeric characters, blank spaces and underscores
            # Error(0x2034): Invalid character in alias
            tolog(Failprompt + aliasName)
            FailFlag = True

    if FailFlag:
        tolog('Modify subsys alias fail')
        tolog(Fail)
    else:
        tolog('Modify subsys alias pass')
        tolog(Pass)


def modifyAndVerifyRedundancyType(c):
    checkResult = ''
    result = tuple()
    FailFlag = False
    # LUN affinity should be disabled before the following execution
    # in new DS, LUN affinity is enabled and cannot be changed.

    tolog("Modify and Verify RedundancyType setting: ")
    lunaffinityresult=SendCmd(c,"ctrl -v")
    if "LUNAffinity: Enabled" in lunaffinityresult:
        SendCmd(c,"ctrl -a mod -s \"lunaffinity=disable\"")

    for i in range(2):

        # determine the original Redundancy type
        OrigResult = SendCmd(c, "subsys -v")
        if "RedundancyType: Active-Active" in OrigResult:
            OrigRedundancyType = "Active-Active"
        else:
            OrigRedundancyType = "Active-Standby"

        if OrigRedundancyType == "Active-Active":
            result = SendCmd(c, 'subsys -a mod -s "redundancytype=active-standby"')
        else:
            result = SendCmd(c, 'subsys -a mod -s "redundancytype=active-active"')

        checkResult = SendCmd(c, "shutdown -a restart")
        from time import sleep
        sleep(200)
        from ssh_connect import ssh_conn

        cnew, sshnew = ssh_conn()
        RewResult = SendCmd(cnew, "subsys -v")
        if "RedundancyType: Active-Active" in RewResult:
            NewRedundancyType = "Active-Active"
        else:
            NewRedundancyType = "Active-Standby"

        if not ("Cachemirroring and RedundancyType setting change will take effect on next"
                in result and 'Error' not in checkResult):
            FailFlag = True

        if not (OrigRedundancyType not in RewResult):
            tolog(Failprompt + NewRedundancyType)
            FailFlag = True
        c = cnew

    if FailFlag:
        tolog('Modify and Verify RedundancyType setting fail')
        tolog(Fail)
    else:
        tolog('Modify and Verify RedundancyType setting pass')
        tolog(Pass)
    sshnew.close()


def modifyAndVerifyCachemirroring(c):
    # modify the cachemirroring from enabled to disabled
    # modify the cachemirroring from disabled to enabled
    checkResult = ''
    result = tuple()
    FailFlag = False
    # LUN affinity should be disabled before the following execution

    tolog("Modify and Verify Cachemirroring setting: ")

    for i in range(2):

        # determine the original Redundancy type
        OrigResult = SendCmd(c, "subsys -v")
        if "CacheMirroring: Enabled" in OrigResult:
            Cachemirroring = "Enabled"
        else:
            RCachemirroring = "Disabled"

        if Cachemirroring == "Enabled":
            result = SendCmd(c, 'subsys -a mod -s "cachemirroring=disable"')
        else:
            result = SendCmd(c, 'subsys -a mod -s "cachemirroring=enable"')

        checkResult = SendCmd(c, "shutdown -a restart")
        from time import sleep
        from ssh_connect import ssh_conn
        sleep(200)
        cnew, sshnew = ssh_conn()

        RewResult = SendCmd(cnew, "subsys -v")

        if "CacheMirroring: Enabled" in RewResult:
            Cachemirroring = "Enabled"
        else:
            Cachemirroring = "Disabled"



        if not ("Cachemirroring and RedundancyType setting change will take effect on next"
                in result and 'Error' not in checkResult):
            FailFlag = True
        if not (Cachemirroring not in OrigResult):
            tolog(Failprompt + Cachemirroring)
            FailFlag = True
        c = cnew

    if FailFlag:
        tolog('Modify and Verify Cachemirroring setting fail')
        tolog(Fail)
    else:
        tolog('Modify and Verify Cachemirroring setting pass')
        tolog(Pass)
    sshnew.close()


def lockunlockAndVerifySubsys(c):
    # only integer numbers from 1 to 1440 are accepted
    # other chars are also verified
    # use unlock to unlock
    checkResult = ''
    result = ""
    FailFlag = False

    tolog("Lock and verify subsys: ")
    #abnorm_params=['abc', 'Abc',"  ","__","##", "%","*","中文"]
    abnorm_params = ['abc', 'Abc', "  ", "__", "##", "%", "*"]
    tolog("Lock subsym by default")
    result=SendCmd(c, "subsys -a lock")
    if not ("You have owned the lock to the subsystem" in result and
                "The lock will expire in 30 min" in result):
        FailFlag=True
    SendCmd(c, "subsys -a unlock")

    for i in range(1, 1600, 60):

        result = SendCmd(c, "subsys -a lock -t " + str(i))
        checkResult = SendCmd(c, "subsys -a chklock")
        checkunlock=SendCmd(c, "subsys -a unlock")
        # convert the mins to x hr x min
        strtime=""
        hour=1
        min=1
        hour = i / 60
        if i<=1440:
            if hour > 0:
                strtime += "%d hr " % hour
            min = i% 60
            strtime+="%d min" % min
            # print strtime
            if not (
                                "You have owned the lock to the subsystem" in result and (
                                "The lock will expire in " + strtime + " at")  in result and
                            "You have owned the lock to the subsystem" in checkResult and
            "You have released the lock to the subsystem." in checkunlock):
                FailFlag = True
                tolog(Failprompt+ str(i))
        else:
            if not ("Invalid lock time" in result and
                        "You do not own the lock to the subsystem" in checkResult and
                    "Current session does not own the lock to the subsystem" in checkunlock):
                FailFlag = True
                tolog(Failprompt + str(i))

    for each in abnorm_params:
        result = SendCmd(c, "subsys -a lock -t " + each)
        if not ("invalid integer" in result and "Error" in result and
                        "Invalid input for integer parameter" in result):
            FailFlag = True
            tolog(Failprompt + each)

    if FailFlag:
        tolog('lock and verify subsys fail')
        tolog(Fail)
    else:
        tolog('lock and verify subsys pass')
        tolog(Pass)

def renewlockunlockandverifysubsys(c):
    # only integer numbers from 1 to 1440 are accepted
    # other chars are also verified
    # use unlock -f to unlock
    # verify expired lock renew
    checkResult = ''
    result = ""
    FailFlag = False
    #abnorm_params=['abc', 'Abc',"  ","__","##", "%","*","中文"]
    abnorm_params = ['abc', 'Abc', "__", "##", "%", "*"]
    SendCmd(c, "subsys -a unlock")
    tolog("Renew Lock and verify subsys: ")

    for i in range(1, 1600, 60):

        SendCmd(c, "subsys -a lock -t 1")
        result=SendCmd(c,"subsys -a lock -r -t " + str(i))
        checkResult = SendCmd(c, "subsys -a chklock")
        checkunlock=SendCmd(c, "subsys -a unlock -f")
        # convert the mins to x hr x min
        strtime=""
        hour=1
        min=1
        hour = i / 60
        if i<=1440:
            if hour > 0:
                strtime += "%d hr " % hour
            min = i% 60
            strtime+="%d min" % min
            # print strtime
            if not (
                                "You have owned the lock to the subsystem." in result and (
                                "The lock will expire in " + strtime + " at")  in result and
                            "You have owned the lock to the subsystem." in checkResult and
            "You have released the lock to the subsystem." in checkunlock):
                FailFlag = True
                tolog(Failprompt + str(i))
        else:
            if not ("Invalid lock time" in result and "Error (0x402): Invalid parameter" in result and
                        "You have owned the lock to the subsystem." in checkResult and
                            "You have released the lock to the subsystem" in checkunlock):
                FailFlag = True
                tolog(Failprompt+str(i))

    for each in abnorm_params:
        SendCmd(c, "subsys -a lock -t 1")
        result = SendCmd(c, "subsys -a lock -r -t " + each)
        if not ("invalid integer" in result and "Error" in result and
                        "Invalid input for integer parameter" in result):
            FailFlag=True
            tolog(Failprompt+each)

    SendCmd(c, "subsys -a unlock -f")
    SendCmd(c, "subsys -a lock -t 1")
    import time
    time.sleep(60)
    result = SendCmd(c, "subsys -a lock -r -t 2")
    if not ("Error" in result and "Error (0x110): The lock has expired" in result):
        tolog(Failprompt + "expired lock")
        FailFlag = True

    if FailFlag:
        tolog('renew lock and verify subsys fail')
        tolog(Fail)
    else:
        tolog('renew lock and verify subsys pass')
        tolog(Pass)

def verfiysubsyshelp(c):
    checkResult = ''
    result = tuple()
    FailFlag = False
    tolog("Verify Subsys Help: ")
    result = SendCmd(c,'subsys -h'),SendCmd(c,'subsys -h123')

    for each in result:
        print each
        if not ('subsys' in each and'Usage' in each and 'Summary' in each and 'to display info page by page' in each):
            FailFlag = True


    if FailFlag:
        tolog('Verify Subsys Help fail')
        tolog(Fail)
    else:
        tolog('Verify Subsys Help pass')
        tolog(Pass)

