# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
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
server = '10.84.2.146'
uname = 'administrator'
pwd = 'password'
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


# from send_cmd import SendCmd
# from ssh_connect import ssh_conn
from ssh_cmd import SendCmd
if __name__ == "__main__":
    # dev key

    new_adminjl_key = 'bc473e34c21e2fe7161dc8374274744b'
    # old_adminjl_key='389c56387aeb06780067649462eb5327'
    # testerjl_key='953b574d1494e53853a7c3b195fda362'
    # tester1_key='ee394318962169dfedbbd30588c3d5ce'
    # # new_testlink="http://192.168.252.141/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
    new_ip_testlink = "http://10.10.10.3/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
    tls = testlink.TestlinkAPIClient(new_ip_testlink, new_adminjl_key)
    # gtls = testlink.TestlinkAPIGeneric("http://192.168.252.141/testlink/lib/api/xmlrpc/v1/xmlrpc.php",
    #                                  "389c56387aeb06780067649462eb5327")
    # test case notes
    Notes = 'testlink.notes'
    #c,ssh=ssh_conn()
    # print tls.whatArgs('getTestCase')

    # build names to be updated before run this script
    # TC_build_name_MAC='4.02.0000.01'
    # TC_build_name_WIN='2.00.0000.16'
    executed_number = 0
    executed_fail_number = 0
    executed_pass_number = 0
    # get test project
    # 20161201 add for filtering the project plan that could be executed by other people.
    # planname = raw_input('please input the test plan name to be executed:')
    cmd = ''
    Notes = 'testlink.notes'

    for project in tls.getProjects():
        # print project
        if project['name'] == 'Hyperion':
            # print project['name'],tls.getProjectTestPlans(1)
            # print 'total tls.getProjectTestPlans',tls.getProjectTestPlans(821)
            # print project
            # print project['name']
            # print project['id']
            # get test plan ID
            # getProjectTestPlans should use project id to display related info
            # the project id is from bitnami_testlink.testprojects 2016-12-16
            #print tls.getProjectTestPlans
            for testplan in tls.getProjectTestPlans(821):

                #if testplan['name'] == '0cli cmd testcases sequence issue':  # 2016.11.24 represent the active test plan testplan['active']=='1' and

                print testplan['name']
                tcdict = tls.getTestCasesForTestPlan(testplan['id'])
                # list each test case ID


                # list each test case by it's test case ID
                print "The test cases under " + testplan['name'] + " of " + project['name'] + " are as following:\n"
                # print type(tcdict)
                if type(tcdict) == dict:
                    tcdict_x = sorted(tcdict.items())
                    #print tcdict_x
                    for eachtestcase in tcdict_x:
                        # for eachtestcase in tcdict.keys():
                        # eachtestcase is tuple type, as following
                        # ('1102', {'6': {'tcase_id': '1102', 'status': '1', 'exec_id': '0', 'tcversion_id': '1103', 'exec_on_tplan': '',
                        # 'platform_id': '6', 'exec_on_build': '', 'execution_duration': '', 'tc_id': '1102', 'tcversion_number': '',
                        # 'execution_type': '1', 'tcase_name': 'bgasched -a list', 'version': '1', 'feature_id': '920', 'full_external_id':
                        # 'Hy-41', 'external_id': '41', 'platform_name': 'subsystem', 'execution_order': '10000', 'exec_status': 'n'}})

                        # print tcdict.get(eachtestcase)
                        # print '------------------------\n'
                        # list test cases by platform
                        # 2016-12-20
                        # http://192.168.252.175:8888/browse/AUT-4
                        # The test cases in one test case suite should be executed in original order. Otherwise,
                        # some cmd cannot be executed successfully because no requisites are met.

                        # print eachtestcase[1]['6']['platform_id']
                        TC_Platform = eachtestcase[1]['6']

                        Platform_Name = TC_Platform['platform_name']
                        TC_Name = TC_Platform['tcase_name']
                        TC_execution = TC_Platform['exec_status']

                        # print '\n'
                        # print '--------------------------------'
                        # print "This test case is to be executed"
                        # print TC_Name + " on " + Platform_Name

                        tcsteps = tls.getTestCase(TC_Platform['tcase_id'])[0]['steps']
                        # if the text contains some special char, such as '\x1b[D \x1b[D', the update to
                        # testlink will be failed as "parsing error, not well formed."

                        steps = [{'step_number': '1',
                                  'notes': '-------------------------------------------------------------\r\nPromise VTrak Command Line Interface (CLI) Utility\r\nVersion: 11.01.0000.63 Build Date: Dec 16, 2016\r\n-------------------------------------------------------------\r\n \r\n-------------------------------------------------------------\r\nType help or ? to display all the available commands\r\n-------------------------------------------------------------\r\n \r\nadministrator@cli> array -a add -p 1,2,3 -l "ID=2,alias=L0,raid=5,capacity=10gb,stripe=512kb,sector=4kb,writepolicy=writeback,readpolicy=nocache,parity=left"\r\nWarning: ld no. 1 - exceeds max sector size, adjust to 512 Bytes\r\nError (0x4021): Physical drive in use\r\n \r\nadministrator@cli> ',
                                  'result': 'p'}, {'step_number': '2',
                                                   'notes': '-------------------------------------------------------------\r\nPromise VTrak Command Line Interface (CLI) Utility\r\nVersion: 11.01.0000.63 Build Date: Dec 16, 2016\r\n-------------------------------------------------------------\r\n \r\n-------------------------------------------------------------\r\nType help or ? to display all the available commands\r\n-------------------------------------------------------------\r\n \r\nadministrator@cli> logdrv -v\r\n \r\n-------------------------------------------------------------------------------\r\nLdId: 0                                LdType: HDD\r\nArrayId: 0                             SYNCed: Yes\r\nOperationalStatus: OK\r\nAlias: \r\nSerialNo: 495345200000000000000000E27BAA63DF120006\r\nWWN: 22bc-0001-5556-12f2               PreferredCtrlId: 1\r\nRAIDLevel: RAID5                       StripeSize: 64 KB\r\nCapacity: 2 GB                         PhysicalCapacity: 3 GB\r\nReadPolicy: NoCache                    WritePolicy: WriteThru\r\nCurrentWritePolicy: WriteThru\r\nNumOfUsedPD: 3                         NumOfAxles: 1\r\nSectorSize: 512 Bytes                  RAID5&6Algorithm: right asymmetric (4)\r\nTolerableNumOfDeadDrivesPerAxle: 1     ParityPace: N/A\r\nRaid6Scheme: N/A\r\nHostAccessibility: Normal\r\nALUAAccessStateForCtrl1: Active/optimized\r\nALUAAccessStateForCtrl2: Standby\r\nAssociationState: no association on this logical drive\r\nStorageServiceStatus: no storage service running\r\nPerfectRebuild: Disabled\r\n \r\nadministrator@cli> ',
                                                   'result': 'p'}]
                        i = 1
                        TC_Result_Steps = list();
                        # print TC_Result_Steps
                        #TC_Result = 'p'
                        stepnote = list()

                        if TC_execution != 'p':
                            #one test case only contains one step, is that function.

                            # for each in tcsteps:
                            open(Notes, 'w').close()
                            stepstr = (string.replace(
                                string.replace(string.replace(tcsteps[0]['actions'], '<p>\n\t', ''), '</p>', ''),
                                '&quot;', '"'))

                            func = stepstr.split('\n')
                            abc = getattr(Buzzer, func[0])
                            abc()
                            # cmd = (string.replace(
                            #     string.replace(string.replace(each['actions'], '<p>\n\t', ''), '</p>', ''),
                            #     '&quot;', '"'))
                            # if cmd != '' and cmd[0] != '#':
                            #     #print cmd
                            #     stepnote = SendCmd(cmd)
                            # TC_Result=Verify_cmd_result(cmd,stepnote)
                            fp= open(Notes,'r')
                            note=fp.read()
                            fp.close()

                            while "'result':" in note:
                                if "'result': 'f'" in note:
                                    TC_Result = 'f'
                                    note = string.replace(note, "'result': 'f'",'')
                                else:
                                    TC_Result = 'p'
                                    note = string.replace(note, "'result': 'p'", '')

                            TC_Result_Steps.append(
                                {'step_number': '1', 'result': TC_Result, 'notes': note})
                            # i += 1

                            buildnamelist = tls.getBuildsForTestPlan(testplan['id'])
                            buildname = buildnamelist[0]['name']

                            # determine the test final result
                            # get information from TC_Result_Steps
                            # for each_step_result in TC_Result_Steps:
                            #         # print 'this is each step result'
                            #
                            #         # print "each_step_result.get('result')", each_step_result.get('result')
                            #     if each_step_result.get('result') != 'p':
                            #         TC_Result = 'f'
                            #         break
                            #     else:
                            #         TC_Result = 'p'

                            # update test result remotely using API
                            # print 'TC_Result',TC_Result

                            Update_timestamp = (
                                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                            # duration_min = getduration(str(TC_execution_duration))


                            # print 'tc result steps', TC_Result_Steps
                            # getExecution = tls.reportTCResult('842', '822',
                            #                                       '11.01.0000.62', 'p',
                            #                                       'notes', guess=True,
                            #                                       testcaseexternalid='2',
                            #                                       platformname='subsystem',
                            #                                       execduration='10',
                            #                                       timestamp='2016-12-19 11:11:33',
                            #                                       steps='ok')


                            getExecution = tls.reportTCResult(TC_Platform['tcase_id'], testplan['id'],
                                                              buildname, TC_Result,
                                                              'notes', guess=True,
                                                              testcaseexternalid=TC_Platform['external_id'],
                                                              platformname=TC_Platform['platform_name'],
                                                              execduration='1',
                                                              timestamp=Update_timestamp,
                                                              steps=TC_Result_Steps)

                                        # updated to testlink successfully.
                        # ssh.close()
