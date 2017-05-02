# -*- coding: utf-8 -*-
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import os
import sys
import testlink
import subprocess
import string
import datetime
import Buzzer
#from Buzzer import verifyBuzzerInfo


# The initial version is from Nov 4, 2016
# get the basic ideas about the testlink API
# get basic info about the project, test plan, test suite, test case
# retrieve the test cases to be executed on specific platforms
# then execute the test cases on specific platforms
# update the test case result to testlink
import glob

def getduration(timestr):
    sec_min = 0
    timelist = list()
    timelist = string.split(timestr, ':')

    if int(timelist[2]) >= 30:
        sec_min = 1
    min = int(timelist[0]) * 60 + int(timelist[1]) + sec_min

    return min

def run_function(function):
    function()
    # verifyBuzzerInfo()

from sgmllib import SGMLParser

class URLLister(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []

    def start_a(self, attrs):
        href = [v for k, v in attrs if k=='href']
        if href:
            self.urls.extend(href)

from HTMLParser import HTMLParser
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


from ssh_connect import ssh_conn
import importlib

#import thread
#import threading

# def raw_input_with_timeout(prompt, timeout):
#
#     timer = threading.Timer(timeout, thread.interrupt_main)
#     astring = "jacky"
#     try:
#         timer.start()
#         astring = raw_input(prompt)
#     except KeyboardInterrupt:
#         pass
#     timer.cancel()
#     return astring

import signal

class AlarmException(Exception):
    pass

def alarmHandler(signum, frame):
    raise AlarmException

def nonBlockingRawInput(prompt='', timeout=5):
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.alarm(timeout)
    try:
        text = raw_input(prompt)
        signal.alarm(0)
        return text
    except AlarmException:
        print '\nPrompt timeout.  Continuing with default name...'
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return "robot"



if __name__ == "__main__":

    lname=nonBlockingRawInput("Only the test cases assgined to you will be executed, please input your name:",1)

    jacky = 'bc473e34c21e2fe7161dc8374274744b'
    zach="1e2a6e7af20e5c274174ff68e2ba63a2"
    hulda='bc473e34c21e2fe7161dc8374274744b'
    robot="31c13726fc2bae727aa02faaaa574892"
    if lname=="jacky":
        new_adminjl_key= jacky
    elif lname=="zach":
        new_adminjl_key = zach
    elif lname=="hulda":
        new_adminjl_key=hulda
    else:
        new_adminjl_key = robot

    # # new_testlink="http://192.168.252.175/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
    #new_ip_testlink = "http://10.10.10.3/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
    new_ip_testlink = "http://192.168.252.175/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
    tls = testlink.TestlinkAPIClient(new_ip_testlink, new_adminjl_key)

    # test case notes
    Notes = 'testlink.notes'
    c,ssh=ssh_conn()
    # print tls.whatArgs('getTestCase')

    # build names to be updated before run this script
    # TC_build_name_MAC='4.02.0000.01'
    # TC_build_name_WIN='2.00.0000.16'
    # executed_number = 0
    # executed_fail_number = 0
    # executed_pass_number = 0
    # get test project
    # 20161201 add for filtering the project plan that could be executed by other people.
    # planname = raw_input('please input the test plan name to be executed:')
    cmd = ''
    stepsnum=0
    Notes = 'testlink.notes'
    #print tls.whatArgs('getTestCasesForTestSuite')
    #print tls.whatArgs('createBuild')
    #print tls.whatArgs("unassignTestCaseExecutionTask")
    NeedRun=False

    for project in tls.getProjects():
        # print project
        if project['name'] == 'HyperionDS':

            #print tls.getProjectTestPlans

            #print tls.whatArgs('getTestCasesForTestSuite')
            # get test suites for the project
            #
            #print tls.getFirstLevelTestSuitesForTestProject(project['id'])

            testsuiteID= tls.getFirstLevelTestSuitesForTestProject(project['id'])[-1]['id']
            hastestsuite=False
            testsuite=tls.getTestCasesForTestSuite(testsuiteID,True,'full')


            for testplan in tls.getProjectTestPlans(1426):
                # changed from 821 to 1426 on April 13th, 2017

                #if testplan['name'] == '0cli cmd testcases sequence issue':  # 2016.11.24 represent the active test plan testplan['active']=='1' and

                #print testplan['name']

                tcdict = tls.getTestCasesForTestPlan(testplan['id'])
                # list each test case ID


                # list each test case by it's test case ID

                if type(tcdict) == dict:
                    tcdict_x = sorted(tcdict.items())


                    for eachtestcase in tcdict_x:


                        #print tcdict.get(eachtestcase)
                        # list test cases by platform
                        # 2016-12-20
                        # http://192.168.252.175:8888/browse/AUT-4
                        # The test cases in one test case suite should be executed in original order. Otherwise,
                        # some cmd cannot be executed successfully because no requisites are met.

                        # print eachtestcase[1]['6']['platform_id']
                        testcaseid=eachtestcase[0]
                        # print eachtestcase
                        #modified on April 13th, 2017
                        #TC_Platform = eachtestcase[1]['6']
                        #

                        for key in eachtestcase[1]:
                            if key!='12':
                                continue
                            else:
                                TC_Platform = eachtestcase[1]['12']

                                Platform_Name = TC_Platform['platform_name']
                                TC_Name = TC_Platform['tcase_name']
                                TC_execution = TC_Platform['exec_status']



                                tcsteps = tls.getTestCase(TC_Platform['tcase_id'])[0]['steps']
                                # if the text contains some special char, such as '\x1b[D \x1b[D', the update to
                                # testlink will be failed as "parsing error, not well formed."
                                # this will be processed in send_cmd

                                steps = [{'step_number': '1',
                                          'notes': '-------------------------------------------------------------\r\nPromise VTrak Command Line Interface (CLI) Utility\r\nVersion: 11.01.0000.63 Build Date: Dec 16, 2016\r\n-------------------------------------------------------------\r\n \r\n-------------------------------------------------------------\r\nType help or ? to display all the available commands\r\n-------------------------------------------------------------\r\n \r\nadministrator@cli> array -a add -p 1,2,3 -l "ID=2,alias=L0,raid=5,capacity=10gb,stripe=512kb,sector=4kb,writepolicy=writeback,readpolicy=nocache,parity=left"\r\nWarning: ld no. 1 - exceeds max sector size, adjust to 512 Bytes\r\nError (0x4021): Physical drive in use\r\n \r\nadministrator@cli> ',
                                          'result': 'p'}, {'step_number': '2',
                                                           'notes': '-------------------------------------------------------------\r\nPromise VTrak Command Line Interface (CLI) Utility\r\nVersion: 11.01.0000.63 Build Date: Dec 16, 2016\r\n-------------------------------------------------------------\r\n \r\n-------------------------------------------------------------\r\nType help or ? to display all the available commands\r\n-------------------------------------------------------------\r\n \r\nadministrator@cli> logdrv -v\r\n \r\n-------------------------------------------------------------------------------\r\nLdId: 0                                LdType: HDD\r\nArrayId: 0                             SYNCed: Yes\r\nOperationalStatus: OK\r\nAlias: \r\nSerialNo: 495345200000000000000000E27BAA63DF120006\r\nWWN: 22bc-0001-5556-12f2               PreferredCtrlId: 1\r\nRAIDLevel: RAID5                       StripeSize: 64 KB\r\nCapacity: 2 GB                         PhysicalCapacity: 3 GB\r\nReadPolicy: NoCache                    WritePolicy: WriteThru\r\nCurrentWritePolicy: WriteThru\r\nNumOfUsedPD: 3                         NumOfAxles: 1\r\nSectorSize: 512 Bytes                  RAID5&6Algorithm: right asymmetric (4)\r\nTolerableNumOfDeadDrivesPerAxle: 1     ParityPace: N/A\r\nRaid6Scheme: N/A\r\nHostAccessibility: Normal\r\nALUAAccessStateForCtrl1: Active/optimized\r\nALUAAccessStateForCtrl2: Standby\r\nAssociationState: no association on this logical drive\r\nStorageServiceStatus: no storage service running\r\nPerfectRebuild: Disabled\r\n \r\nadministrator@cli> ',
                                                           'result': 'p'}]

                                TC_Result_Steps = list()
                                stepnote = list()
                            # Added on April 18th, 2017
                            # to determine last execution on which build
                            # if the build id is smaller than current build,
                            # rerun the test case

                            buildnamelist = tls.getBuildsForTestPlan(testplan['id'])
                            buildname = buildnamelist[-1]['name']
                            newbuildnum = open("/home/work/jackyl/Scripts/clitest/buildnum", "r").readline().rstrip()
                            # print "newbuildnum is %s, currentbuild is %s" %(newbuildnum,buildname)

                            if buildname != newbuildnum:
                                buildname = tls.createBuild(testplan['id'], newbuildnum, "auto")

                            buildnamelist = tls.getBuildsForTestPlan(testplan['id'])
                            buildname = buildnamelist[-1]['name']
                            testplanexec = tls.getTestCasesForTestPlan(testplan['id'])
                            exec_onbuild = testplanexec[TC_Platform['tcase_id']]['12']['exec_on_build']

                            if buildnamelist[-1]['id'] > exec_onbuild:
                                NeedRun=True
                            # added this part on April 15th, 2017
                            # for build acceptance testing
                            # new build will be created through the following line
                            # buildnumber


                                #                                   'Notes for the Build',
                                #                                   releasedate="2016-12-31")


                            if NeedRun or TC_Name=="build_verification":# or TC_execution != 'f':
                                    #one test case only contains one step, is that function.
                                    # 2016.12.29
                                    # to determine testcases's testsuite id
                                    # print testsuite

                                    for each in testsuite:
                                        if each['id']==testcaseid:
                                            testsuitename=each['tsuite_name']
                                            hastestsuite=True

                                            # added on April 25th, 2017
                                            # to execute test cases by assigned user
                                    buildnamelist = tls.getBuildsForTestPlan(testplan['id'])
                                    buildname = buildnamelist[-1]['name']
                                    #print testplan['id'],eachtestcase[1]['12']['full_external_id'],buildname,eachtestcase[1]['12']
                                    # print tls.whatArgs("assignTestCaseExecutionTask")
                                    # print tls.whatArgs("getTestCaseAssignedTester")

                                    #aaaa = tls.getTestCasesForTestPlan(testplan['id'])
                                    #bbbb=tls.assignTestCaseExecutionTask("jacky", testplan['id'], eachtestcase[1]['12']['full_external_id'], buildname=buildname,platformname=Platform_Name)
                                    loginname=tls.getTestCaseAssignedTester(testplan['id'], eachtestcase[1]['12']['full_external_id'], buildname=buildname,platformname=Platform_Name)


                                    if hastestsuite and (lname==loginname[0]['login'] or lname=="robot"):
                                        print "The test cases under " + testplan['name'] + " of " + project[
                                            'name'] + " are as following:\n"
                                        start = time.time()
                                        # convert the testsuite name into module that will be imported into
                                        TSuiteName = importlib.import_module(testsuitename, package="Tasks")
                                        #print tls.getTestCase(TC_Platform['tcase_id'])
                                        # if >= 2 steps, 2017-01-06
                                        stepsnum=len(tcsteps)
                                        for i in range(stepsnum):
                                            open(Notes, 'w').close()
                                            stepstr = (string.replace(
                                                string.replace(string.replace(tcsteps[i]['actions'], '<p>\n\t', ''), '</p>', ''),
                                                '&quot;', '"'))

                                            func = stepstr.split('\n')

                                            # convert the stepname into function that will be executed in the above module
                                            abc = getattr(TSuiteName, func[0],func[1])
                                            # if some parameters are to be passed into
                                            # please write the parameter on second line
                                            # it will be func[1]
                                            parameter=func[1]
                                            # print parameter
                                            # if there's restart action in the function
                                            # the c is changed
                                            # 2016-12-30 to reestablish the ssh connection
                                            if ssh.get_transport().is_active()!=True:
                                                c,ssh=ssh_conn()
                                            if parameter:
                                                abc(c,parameter)
                                            else:
                                                abc(c)

                                            # read testcase notes from Notes
                                            fp= open(Notes,'r')
                                            note=fp.read()
                                            fp.close()

                                            # determine the execution result that will be updated to testlink.
                                            while "'result':" in note:
                                                if "'result': 'f'" in note:
                                                    step_Result = 'f'
                                                    note = string.replace(note, "'result': 'f'",'')
                                                else:
                                                    step_Result = 'p'
                                                    note = string.replace(note, "'result': 'p'", '')

                                            TC_Result_Steps.append(
                                                {'step_number': str(i+1), 'result': step_Result, 'notes': note})

                                        for each in TC_Result_Steps:
                                            if each['result']!='p':
                                                TC_Result='f'
                                                break
                                            else:
                                                TC_Result='p'



                                        # update test result remotely using API


                                        Update_timestamp = (
                                            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                                        # duration_min = getduration(str(TC_execution_duration))
                                        elasped = time.time() - start
                                        duration_min=str(elasped/60)
                                        buildnamelist = tls.getBuildsForTestPlan(testplan['id'])
                                        buildname = buildnamelist[-1]['name']

                                        #TC_Result_Steps=[{'step_number': '0', 'notes': 'step1', 'result': 'f'}, {'step_number': '1', 'notes': 'step2 ', 'result': 'p'}]
                                        getExecution = tls.reportTCResult(TC_Platform['tcase_id'], testplan['id'],
                                                                          buildname, TC_Result,
                                                                          'automated test cases', guess=True,
                                                                          testcaseexternalid=TC_Platform['external_id'],
                                                                          platformname=TC_Platform['platform_name'],
                                                                          execduration=duration_min,
                                                                          timestamp=Update_timestamp,
                                                                          steps=TC_Result_Steps)


                                        if TC_Name=="build_verification":
                                            serv = "MjExLjE1MC42NS44MQ=="
                                            u = "amFja3kubGlAY24ucHJvbWlzZS5jb20="
                                            p = "NzcwMjE0WHA="
                                            import smtplib
                                            import urllib

                                            # Import the email modules we'll need
                                            from email.mime.text import MIMEText


                                            if getExecution[0]['status']:

                                                link="http://192.168.252.175/testlink/lib/execute/execPrint.php?id="+str(getExecution[0]['id'])



                                                fp = urllib.urlopen(link)


                                                msg=MIMEText(strip_tags(fp.read()).replace(".notprintable { display:none;}","").replace("lnl.php?type=exec=","execPrint.php?id=").replace("<!-- var fRoot = 'http://192.168.252.175/testlink/lib/execute/'; -->",""))

                                                msg[
                                                    'Subject'] = 'Build verification testing on %s is completed, the result is %s, please check the link for detail' % (buildname,TC_Result)
                                                msg['From'] = 'jacky.li@cn.promise.com'
                                                msg['To'] = 'jacky.li@cn.promise.com'
                                                # rec = ['jacky.li@cn.promise.com', 'hulda.zhao@cn.promise.com']
                                                rec = ['jacky.li@cn.promise.com']
                                                # Send the message via our own SMTP server, but don't include the
                                                # envelope header.
                                                u = u.decode('base64')
                                                serv = serv.decode('base64')
                                                p = p.decode('base64')

                                                s = smtplib.SMTP(serv)
                                                s.login(u, p)
                                                s.sendmail(msg['From'], rec, msg.as_string())


ssh.close()
