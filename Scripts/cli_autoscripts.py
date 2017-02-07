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


from ssh_connect import ssh_conn
import importlib

if __name__ == "__main__":
    # dev key

    new_adminjl_key = 'bc473e34c21e2fe7161dc8374274744b'

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

            #print tls.whatArgs('getTestCasesForTestSuite')
            # get test suites for the project
            #
            testsuiteID= tls.getFirstLevelTestSuitesForTestProject(project['id'])[1]['id']
            hastestsuite=False
            testsuite=tls.getTestCasesForTestSuite(testsuiteID,True,'full')
            # print testsuite
            # {'node_order': '1000', 'is_open': '1', 'id': '1315', 'node_type_id': '3', 'layout': '1',
            #  'tc_external_id': '78', 'parent_id': '1314', 'version': '1', 'estimated_exec_duration': '',
            #  'updater_id': '1', 'status': '1', 'tsuite_name': 'Buzzer', 'importance': '2',
            #  'modification_ts': '2016-12-23 15:29:00', 'execution_type': '1', 'preconditions': '', 'active': '1',
            #  'creation_ts': '2016-12-23 14:40:50', 'node_table': 'testcases', 'tcversion_id': '1316',
            #  'name': 'list buzz status', 'summary': '', 'steps': [
            #     {'step_number': '1', 'actions': '<p>\n\tverifyBuzzerInfo</p>\n', 'execution_type': '1', 'active': '1',
            #      'id': '1317', 'expected_results': ''}], 'author_id': '1', 'external_id': 'Hy-78'}, {
            #     'node_order': '1001', 'is_open': '1', 'id': '1318', 'node_type_id': '3', 'layout': '1',
            #     'tc_external_id': '79', 'parent_id': '1314', 'version': '1', 'estimated_exec_duration': '',
            #     'updater_id': '1', 'status': '1', 'tsuite_name': 'Buzzer', 'importance': '2',
            #     'modification_ts': '2016-12-23 17:46:57', 'execution_type': '1', 'preconditions': '', 'active': '1',
            #     'creation_ts': '2016-12-23 14:42:06', 'node_table': 'testcases', 'tcversion_id': '1319',
            #     'name': 'Enable buzz', 'summary': '', 'steps': [
            #         {'step_number': '1', 'actions': '<p>\n\tverifyEnableBuzzer</p>\n', 'execution_type': '1',
            #          'active': '1', 'id': '1320', 'expected_results': ''}], 'author_id': '1', 'external_id': 'Hy-79'}, {
            #     'node_order': '1002', 'is_open': '1', 'id': '1321', 'node_type_id': '3', 'layout': '1',
            #     'tc_external_id': '80', 'parent_id': '1314', 'version': '1', 'estimated_exec_duration': '',
            #     'updater_id': '1', 'status': '1', 'tsuite_name': 'Buzzer', 'importance': '2',
            #     'modification_ts': '2016-12-23 17:47:19', 'execution_type': '1', 'preconditions': '', 'active': '1',
            #     'creation_ts': '2016-12-23 14:42:52', 'node_table': 'testcases', 'tcversion_id': '1322',
            #     'name': 'Turn on buzz', 'summary': '', 'steps': [
            #         {'step_number': '1', 'actions': '<p>\n\tverifyTurnOnBuzzer</p>\n', 'execution_type': '1',
            #          'active': '1', 'id': '1323', 'expected_results': ''}], 'author_id': '1', 'external_id': 'Hy-80'}, {
            #     'node_order': '1003', 'is_open': '1', 'id': '1324', 'node_type_id': '3', 'layout': '1',
            #     'tc_external_id': '81', 'parent_id': '1314', 'version': '1', 'estimated_exec_duration': '',
            #     'updater_id': '1', 'status': '1', 'tsuite_name': 'Buzzer', 'importance': '2',
            #     'modification_ts': '2016-12-23 17:47:43', 'execution_type': '1', 'preconditions': '', 'active': '1',
            #     'creation_ts': '2016-12-23 14:43:23', 'node_table': 'testcases', 'tcversion_id': '1325',
            #     'name': 'Turn off buzz', 'summary': '', 'steps': [
            #         {'step_number': '1', 'actions': '<p>\n\tverifyTurnOffBuzzer</p>\n', 'execution_type': '1',
            #          'active': '1', 'id': '1326', 'expected_results': ''}], 'author_id': '1', 'external_id': 'Hy-81'}, {
            #     'node_order': '1004', 'is_open': '1', 'id': '1329', 'node_type_id': '3', 'layout': '1',
            #     'tc_external_id': '83', 'parent_id': '1314', 'version': '1', 'estimated_exec_duration': '',
            #     'updater_id': '1', 'status': '1', 'tsuite_name': 'Buzzer', 'importance': '2',
            #     'modification_ts': '2016-12-23 17:48:25', 'execution_type': '1', 'preconditions': '', 'active': '1',
            #     'creation_ts': '2016-12-23 14:46:00', 'node_table': 'testcases', 'tcversion_id': '1330',
            #     'name': 'Disable buzz', 'summary': '', 'steps': [
            #         {'step_number': '1', 'actions': '<p>\n\tverifyDisableBuzzer</p>\n', 'execution_type': '1',
            #          'active': '1', 'id': '1331', 'expected_results': ''}], 'author_id': '1', 'external_id': 'Hy-83'}, {
            #     'node_order': '1005', 'is_open': '1', 'id': '1332', 'node_type_id': '3', 'layout': '1',
            #     'tc_external_id': '84', 'parent_id': '1314', 'version': '1', 'estimated_exec_duration': '',
            #     'updater_id': '1', 'status': '1', 'tsuite_name': 'Buzzer', 'importance': '2',
            #     'modification_ts': '2016-12-23 18:28:59', 'execution_type': '1', 'preconditions': '', 'active': '1',
            #     'creation_ts': '2016-12-23 14:46:35', 'node_table': 'testcases', 'tcversion_id': '1333',
            #     'name': 'Turn on buzz while buzz disabled', 'summary': '', 'steps': [
            #         {'step_number': '1', 'actions': '<p>\n\tVerifyTurnonBuzzerDisabled</p>\n', 'execution_type': '1',
            #          'active': '1', 'id': '1334', 'expected_results': ''}], 'author_id': '1', 'external_id': 'Hy-84'}, {
            #     'node_order': '1006', 'is_open': '1', 'id': '1335', 'node_type_id': '3', 'layout': '1',
            #     'tc_external_id': '85', 'parent_id': '1314', 'version': '1', 'estimated_exec_duration': '',
            #     'updater_id': '1', 'status': '1', 'tsuite_name': 'Buzzer', 'importance': '2',
            #     'modification_ts': '2016-12-23 18:13:24', 'execution_type': '1', 'preconditions': '', 'active': '1',
            #     'creation_ts': '2016-12-23 14:47:47', 'node_table': 'testcases', 'tcversion_id': '1336',
            #     'name': 'Invalid parameter', 'summary': '', 'steps': [
            #         {'step_number': '1', 'actions': '<p>\n\tverifyBuzzerInvalidParameter</p>\n', 'execution_type': '1',
            #          'active': '1', 'id': '1346', 'expected_results': ''}], 'author_id': '1', 'external_id': 'Hy-85'}, {
            #     'node_order': '1007', 'is_open': '1', 'id': '1341', 'node_type_id': '3', 'layout': '1',
            #     'tc_external_id': '86', 'parent_id': '1314', 'version': '1', 'estimated_exec_duration': '',
            #     'updater_id': '1', 'status': '1', 'tsuite_name': 'Buzzer', 'importance': '2',
            #     'modification_ts': '2016-12-26 16:55:38', 'execution_type': '1', 'preconditions': '', 'active': '1',
            #     'creation_ts': '2016-12-23 14:49:16', 'node_table': 'testcases', 'tcversion_id': '1342',
            #     'name': 'invalid action', 'summary': '', 'steps': [
            #         {'step_number': '1', 'actions': '<p>\n\tVerifyBuzzerInvalidActions</p>\n', 'execution_type': '1',
            #          'active': '1', 'id': '1348', 'expected_results': ''}], 'author_id': '1', 'external_id': 'Hy-86'}, {
            #     'node_order': '1008', 'is_open': '1', 'id': '1349', 'node_type_id': '3', 'layout': '1',
            #     'tc_external_id': '87', 'parent_id': '1314', 'version': '1', 'estimated_exec_duration': '',
            #     'updater_id': '1', 'status': '1', 'tsuite_name': 'Buzzer', 'importance': '2',
            #     'modification_ts': '2016-12-26 15:25:08', 'execution_type': '1', 'preconditions': '', 'active': '1',
            #     'creation_ts': '2016-12-26 15:24:24', 'node_table': 'testcases', 'tcversion_id': '1350',
            #     'name': 'Buzz help', 'summary': '', 'steps': [
            #         {'step_number': '1', 'actions': '<p>\n\tVerifyBuzzerHelp</p>\n', 'execution_type': '1',
            #          'active': '1', 'id': '1351', 'expected_results': ''}], 'author_id': '1', 'external_id': 'Hy-87'},

            for testplan in tls.getProjectTestPlans(821):

                #if testplan['name'] == '0cli cmd testcases sequence issue':  # 2016.11.24 represent the active test plan testplan['active']=='1' and

                #print testplan['name']

                tcdict = tls.getTestCasesForTestPlan(testplan['id'])
                # list each test case ID


                # list each test case by it's test case ID
                print "The test cases under " + testplan['name'] + " of " + project['name'] + " are as following:\n"
                # print type(tcdict)
                if type(tcdict) == dict:
                    tcdict_x = sorted(tcdict.items())
                    #print tcdict_x
                    for eachtestcase in tcdict_x:

                        # eachtestcase is in tuple type, as following
                        # ('1102', {'6': {'tcase_id': '1102', 'status': '1', 'exec_id': '0', 'tcversion_id': '1103', 'exec_on_tplan': '',
                        # 'platform_id': '6', 'exec_on_build': '', 'execution_duration': '', 'tc_id': '1102', 'tcversion_number': '',
                        # 'execution_type': '1', 'tcase_name': 'bgasched -a list', 'version': '1', 'feature_id': '920', 'full_external_id':
                        # 'Hy-41', 'external_id': '41', 'platform_name': 'subsystem', 'execution_order': '10000', 'exec_status': 'n'}})

                        #print tcdict.get(eachtestcase)
                        # list test cases by platform
                        # 2016-12-20
                        # http://192.168.252.175:8888/browse/AUT-4
                        # The test cases in one test case suite should be executed in original order. Otherwise,
                        # some cmd cannot be executed successfully because no requisites are met.

                        # print eachtestcase[1]['6']['platform_id']
                        testcaseid=eachtestcase[0]
                        TC_Platform = eachtestcase[1]['6']

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

                        TC_Result_Steps = list();
                        stepnote = list()

                        if TC_execution != 'p':# or TC_execution != 'f':
                            #one test case only contains one step, is that function.
                            # 2016.12.29
                            # to determine testcases's testsuite id

                            for each in testsuite:
                                if each['id']==testcaseid:
                                    testsuitename=each['tsuite_name']
                                    hastestsuite=True

                            if hastestsuite:

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
                                    abc = getattr(TSuiteName, func[0])
                                    # if there's restart action in the function
                                    # the c is changed
                                    # 2016-12-30 to reestablish the ssh connection
                                    if ssh.get_transport().is_active()!=True:
                                        c,ssh=ssh_conn()

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

                                buildnamelist = tls.getBuildsForTestPlan(testplan['id'])
                                buildname = buildnamelist[0]['name']

                                # update test result remotely using API


                                Update_timestamp = (
                                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                                # duration_min = getduration(str(TC_execution_duration))


                                #TC_Result_Steps=[{'step_number': '0', 'notes': 'step1', 'result': 'f'}, {'step_number': '1', 'notes': 'step2 ', 'result': 'p'}]
                                getExecution = tls.reportTCResult(TC_Platform['tcase_id'], testplan['id'],
                                                                  buildname, TC_Result,
                                                                  'automated test cases', guess=True,
                                                                  testcaseexternalid=TC_Platform['external_id'],
                                                                  platformname=TC_Platform['platform_name'],
                                                                  execduration='1',
                                                                  timestamp=Update_timestamp,
                                                                  steps=TC_Result_Steps)

ssh.close()
