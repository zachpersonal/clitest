# coding=utf-8
# initial sample work on 2016.12.23
# this section includes verify proper cmd/parameters/options and
# some other boundary or misspelled parameters/options
from  send_cmd import SendCmd
from to_log import tolog
from ssh_connect import ssh_conn
import string

Pass = "'result': 'p'"
Fail = "'result': 'f'"


def verifyTurnOnBuzzer(c):
    checkResult = ''
    result = tuple()
    FailFlag=False
    tolog("Turn on buzzer: ")
    result = SendCmd(c,'buzz -a on'),SendCmd(c,'buzz -aon')
    checkResult = SendCmd(c,'buzz')
    for each in result:
        if 'Error' in each or 'Sounding' not in checkResult:
            FailFlag=True

    if FailFlag:
        tolog('Turn on buzzer fail')
        tolog(Fail)
    else:
        tolog('Turn on buzzer pass')
        tolog(Pass)



def verifyTurnOffBuzzer(c):
    checkResult = ''
    result = tuple()
    FailFlag = False
    tolog("Turn off buzzer: ")
    result = SendCmd(c,'buzz -a off'),SendCmd(c,'buzz -aoff')
    checkResult = SendCmd(c,'buzz')

    for each in result:
        if 'Error' in each or 'Silent' not in checkResult:
            FailFlag = True

    if FailFlag:
        tolog('Turn off buzzer fail')
        tolog(Fail)
    else:
        tolog('Turn off buzzer pass')
        tolog(Pass)



def verifyEnableBuzzer(c):
    checkResult = ''
    result = tuple()
    FailFlag = False
    tolog("Enable buzzer: ")
    result = SendCmd(c,'buzz -a enable'),SendCmd(c,'buzz -aenable')
    checkResult = SendCmd(c,'buzz')

    for each in result:
        if 'Error' in each or 'Yes' not in checkResult:
            FailFlag = True

    if FailFlag:
        tolog('Enable buzzer fail')
        tolog(Fail)
    else:
        tolog('Enable buzzer pass')
        tolog(Pass)



def verifyDisableBuzzer(c):
    checkResult = ''
    result = tuple()
    tolog("Disable buzzer: ")
    FailFlag=False
    result = SendCmd(c,'buzz -a disable'),SendCmd(c,'buzz -adisable')
    checkResult = SendCmd(c,'buzz')

    for each in result:
        if 'Error' in each or 'No' not in checkResult:
            FailFlag = True

    if FailFlag:
        tolog('Disable buzzer fail')
        tolog(Fail)
    else:
        tolog('Disable buzzer pass')
        tolog(Pass)


def verifyBuzzerInfo(c):
    checkResult = ''
    result = tuple()
    FailFlag=False
    tolog("Check buzzer information: ")
    result = SendCmd(c,'buzz'),SendCmd(c,'buzz -a list'),SendCmd(c,'buzz -alist'),
    # checkResult = SendCmd('buzz')
    FailFlag=False
    for each in result:
        if 'Error' in each:
            FailFlag=True


    if FailFlag:
        tolog('Check buzzer info fail')
        tolog(Fail)
    else:
        tolog('Check buzzer info pass')
        tolog(Pass)


def verifyBuzzerInvalidParameter(c):
    checkResult = ''
    result = tuple()
    FailFlag = False
    tolog("Check buzzer Invalid Parameters: ")
    result=SendCmd(c,'buzz abc'),SendCmd(c,'buzz 123')

    for each in result:
        if not ('Error' in each and 'Invalid parameter' in each):
            FailFlag=True

    if FailFlag:
        tolog('Check buzzer Invalid Parameters fail')
        tolog(Fail)
    else:
        tolog('Check buzzer Invalid Parameters pass')
        tolog(Pass)


def VerifyTurnonBuzzerDisabled(c):
    checkResult = ''
    result = tuple()
    SendCmd(c,'buzz -a disable')
    tolog("Turn on buzzer: ")
    result = SendCmd(c,'buzz -a on')
    verifyBuzzerInfo(c)
    if 'Error' in result and 'Buzzer is disabled' in result:
        tolog('Check turn on buzzer when it is disabled pass')
        tolog(Pass)
    else:
        tolog('Check turn on buzzer when it is disabled fail')
        tolog(Fail)

def VerifyBuzzerInvalidActions(c):
    checkResult = ''
    result = tuple()
    FailFlag = False


    result = SendCmd(c,'buzz -alista'),SendCmd(c,'buzz -a 123'),SendCmd(c,'buzz -a test'),SendCmd(c,'buzz -a 你好')
    tolog("Verify Buzzer Invalid Actions: ")
    for each in result:
        if not (('Error' in each) and ('Invalid action' in each)):
            FailFlag = True


    if FailFlag:
        tolog('Check buzzer Invalid Options fail')
        tolog(Fail)
    else:
        tolog('Check buzzer Invalid Options pass')
        tolog(Pass)

def VerifyBuzzerHelp(c):
    checkResult = ''
    result = tuple()
    FailFlag = False
    # buzz -aon should be a misspelled option
    result = SendCmd(c,'buzz -h'),SendCmd(c,'buzz -h123')
    tolog("Verify Buzzer Help: ")
    for each in result:
        print each
        if not ('buzz' in each and'Usage' in each and 'Summary' in each and 'to display info page by page' in each):
            FailFlag = True


    if FailFlag:
        tolog('Verify Buzzer Help fail')
        tolog(Fail)
    else:
        tolog('Verify Buzzer Help pass')
        tolog(Pass)


if __name__ == "__main__":

    c, ssh = ssh_conn()
    verifyTurnOnBuzzer(c)
    verifyTurnOffBuzzer(c)
    verifyEnableBuzzer(c)
    verifyDisableBuzzer(c)
    verifyBuzzerInfo(c)

    VerifyBuzzerInvalidActions(c)
    verifyBuzzerInvalidParameter(c)
    VerifyBuzzerHelp(c)
    ssh.close()