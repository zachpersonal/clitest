# coding=utf-8
# initial sample work on 2016.12.23
# this section includes verify proper cmd/parameters/options and
# some other boundary or misspelled parameters/options
from  ssh_cmd import SendCmd
from to_log import tolog
import string

Pass = "'result': 'p'"
Fail = "'result': 'f'"


def verifyTurnOnBuzzer():
    checkResult = ''
    result = tuple()
    FailFlag=False
    tolog("Turn on buzzer: ")
    result = SendCmd('buzz -a on'),SendCmd('buzz -aon')
    checkResult = SendCmd('buzz')
    for each in result:
        if 'Error' in each or 'Sounding' not in checkResult:
            FailFlag=True

    if FailFlag:
        tolog('Turn on buzzer fail')
        tolog(Fail)
    else:
        tolog('Turn on buzzer pass')
        tolog(Pass)



def verifyTurnOffBuzzer():
    checkResult = ''
    result = tuple()
    FailFlag = False
    tolog("Turn off buzzer: ")
    result = SendCmd('buzz -a off'),SendCmd('buzz -aoff')
    checkResult = SendCmd('buzz')

    for each in result:
        if 'Error' in each or 'Silent' not in checkResult:
            FailFlag = True

    if FailFlag:
        tolog('Turn off buzzer fail')
        tolog(Fail)
    else:
        tolog('Turn off buzzer pass')
        tolog(Pass)



def verifyEnableBuzzer():
    checkResult = ''
    result = tuple()
    FailFlag = False
    tolog("Enable buzzer: ")
    result = SendCmd('buzz -a enable'),SendCmd('buzz -aenable')
    checkResult = SendCmd('buzz')

    for each in result:
        if 'Error' in each or 'Yes' not in checkResult:
            FailFlag = True

    if FailFlag:
        tolog('Enable buzzer fail')
        tolog(Fail)
    else:
        tolog('Enable buzzer pass')
        tolog(Pass)



def verifyDisableBuzzer():
    checkResult = ''
    result = tuple()
    tolog("Disable buzzer: ")
    FailFlag=False
    result = SendCmd('buzz -a disable'),SendCmd('buzz -adisable')
    checkResult = SendCmd('buzz')

    for each in result:
        if 'Error' in each or 'No' not in checkResult:
            FailFlag = True

    if FailFlag:
        tolog('Disable buzzer fail')
        tolog(Fail)
    else:
        tolog('Disable buzzer pass')
        tolog(Pass)


def verifyBuzzerInfo():
    checkResult = ''
    result = tuple()
    FailFlag=False
    tolog("Check buzzer information: ")
    result = SendCmd('buzz'),SendCmd('buzz -a list'),SendCmd('buzz -alist'),
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


def verifyBuzzerInvalidParameter():
    checkResult = ''
    result = tuple()
    FailFlag = False
    tolog("Check buzzer Invalid Parameters: ")
    result=SendCmd('buzz abc'),SendCmd('buzz 123')

    for each in result:
        if 'Error' not in each or 'Invalid parameter' not in each:
            FailFlag=True

    if FailFlag:
        tolog('Check buzzer Invalid Parameters fail')
        tolog(Fail)
    else:
        tolog('Check buzzer Invalid Parameters pass')
        tolog(Pass)


def VerifyTurnonBuzzerDisabled():
    checkResult = ''
    result = tuple()
    SendCmd('buzz -a disable')
    tolog("Turn on buzzer: ")
    result = SendCmd('buzz -a on')
    verifyBuzzerInfo()
    if 'Error' in result and 'Buzzer is disabled' in result:
        tolog('Check turn on buzzer when it is disabled pass')
        tolog(Pass)
    else:
        tolog('Check turn on buzzer when it is disabled fail')
        tolog(Fail)

def VerifyBuzzerInvalidActions():
    checkResult = ''
    result = tuple()
    FailFlag = False


    result = SendCmd('buzz -alista'),SendCmd('buzz -a 123'),SendCmd('buzz -a test'),SendCmd('buzz -a 你好')
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

def VerifyBuzzerHelp():
    checkResult = ''
    result = tuple()
    FailFlag = False
    # buzz -aon should be a misspelled option
    result = SendCmd('buzz -h'),SendCmd('buzz -h123')
    tolog("Verify Buzzer Help: ")
    for each in result:
        if 'Usage' not in each and 'Summary' not in each and 'to display info page by page' not in result:
            FailFlag = True


    if FailFlag:
        tolog('Verify Buzzer Help fail')
        tolog(Fail)
    else:
        tolog('Verify Buzzer Help pass')
        tolog(Pass)


