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
# The initial version is from Nov 4, 2016
# get the basic ideas about the testlink API
# get basic info about the project, test plan, test suite, test case
# retrieve the test cases to be executed on specific platforms
# then execute the test cases on specific platforms
# update the test case result to testlink
import glob
def getduration(timestr):
    sec_min=0
    timelist=list()
    timelist=string.split(timestr, ':')

    if int(timelist[2])>=30:
        sec_min=1
    min=int(timelist[0])*60 + int(timelist[1])+sec_min

    return min

if __name__ == "__main__":
    # dev key

    new_adminjl_key='bc473e34c21e2fe7161dc8374274744b'
    # old_adminjl_key='389c56387aeb06780067649462eb5327'
    # testerjl_key='953b574d1494e53853a7c3b195fda362'
    # tester1_key='ee394318962169dfedbbd30588c3d5ce'
    # # new_testlink="http://192.168.252.141/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
    new_ip_testlink="http://10.10.10.3/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
    tls=testlink.TestlinkAPIClient(new_ip_testlink,new_adminjl_key)
    # gtls = testlink.TestlinkAPIGeneric("http://192.168.252.141/testlink/lib/api/xmlrpc/v1/xmlrpc.php",
    #                                  "389c56387aeb06780067649462eb5327")
    # test case notes
    Notes='testlink.notes'
    # print tls.whatArgs('getTestCase')

    # build names to be updated before run this script
    # TC_build_name_MAC='4.02.0000.01'
    # TC_build_name_WIN='2.00.0000.16'
    executed_number=0
    executed_fail_number=0
    executed_pass_number=0
    # get test project
    # 20161201 add for filtering the project plan that could be executed by other people.
    # planname = raw_input('please input the test plan name to be executed:')
    for project in tls.getProjects():
        if project['name']=='Pegasus':
            #print project
            #print project['name']
            #print project['id']
            # get test plan ID
            # getProjectTestPlans should use project id to display related info
            for testplan in tls.getProjectTestPlans(1):
                # print testplan
                # print "The testplan name is " + testplan['name']
                # print "The testplan ID is " + testplan['id']

                #get test cases for each test plan

                #print tls.getTestCasesForTestPlan(testplan['id'])
                # get the tpye of this data
                # print type(tls.getTestCasesForTestPlan(testplan['id']))

                # get test case ID for each test case
                # print type(testcase)
                # for testcase in tls.getTestCasesForTestPlan(testplan['id']):
                #
                #     print testcase
                try:
                    if  testplan['active']=='1': # and testplan['name']==planname: 2016.11.24 represent the active test plan

                        tcdict = tls.getTestCasesForTestPlan(testplan['id'])
                        # list each test case ID
                        #print tcdict.keys()

                        # list each test case by it's test case ID
                        print "The test cases under " + testplan['name'] + " of " + project['name'] + " are as following:\n"
                        #print type(tcdict)
                        if type(tcdict)==dict:
                            #print tcdict.keys()
                            for eachtestcase in tcdict.keys():
                                # print tcdict.get(eachtestcase)
                                # print '------------------------\n'
                                # list test cases by platform
                                for eachplatform in tcdict.get(eachtestcase):
                                    if type((tcdict.get(eachtestcase)))==dict:

                                        TC_Platform = (tcdict.get(eachtestcase)).get(eachplatform)

                                        Platform_Name = TC_Platform['platform_name']
                                        TC_Name = TC_Platform['tcase_name']
                                        TC_execution = TC_Platform['exec_status']
                                        # TC_build=TC_Platform


                                        # get the test result by assigned tester
                                        # NO success
                                        # result=tls.getTestCaseAssignedTester(testplan['id'],TC_Platform['external_id'],TC_Platform['build_name'])

                                        # print result



                                        # for executed test cases
                                        if TC_execution == 'p' or TC_execution == 'f': # 2016.11.22 re-run the failed test cases//
                                            #print "This test case has been executed as " + TC_execution
                                            print TC_Name + " on " + Platform_Name +' Status: '+ TC_execution
                                            executed_number += 1
                                            if TC_execution == 'p': executed_pass_number+=1
                                            else:
                                                executed_fail_number+=1

                                            #print tls.getTestCase(TC_Platform['tcase_id'])

                                        # for test cases that not executed yet
                                        else:
                                            print '\n'
                                            print '--------------------------------'
                                            print "This test case is to be executed"
                                            print TC_Name + " on " + Platform_Name

                                            #write the platform to text file that will be executed later
                                            Pfile = open('platform.txt', 'w')
                                            print >> Pfile, Platform_Name
                                            Pfile.close()

                                            #will be replaced with multipule thread module to allow more python exec running.
                                            # Nov 10, 2016
                                            # clear test case notes before execute another one.
                                            open(Notes, 'w').close()
                                            os.system("Python.exe " + TC_Name + '.py')

                                            # dealing with notesfile
                                            # put the notes into the testlink steps' notes
                                            # put the pass or fail result to testlink result

                                            stepnote = list()
                                            # empty the file for next testcase
                                            # open(Notes, 'w').close()
                                            tcsteps=tls.getTestCase(TC_Platform['tcase_id'])[0]['steps']
                                            steps = [{'step_number': 1, 'result': 'p', 'notes': 'result note for passed step 1'},{'step_number': 2, 'result': 'f', 'notes': 'result note for failed step 2'}]

                                            # Nov 9, 2016


                                            TC_Result_Steps=list()
                                            TC_execution_duration = datetime.datetime.strptime("2016-11-08 15:48:21",
                                                                                               '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(
                                                "2016-11-08 15:48:21", '%Y-%m-%d %H:%M:%S')


                                            # for each step in test case steps,
                                            # get the note info for each step

                                            # first, get the notes file into a list

                                            with open(Notes) as fp:
                                                for i, line in enumerate(fp):
                                                    stepnote.append(line)



                                            # get the result numbers in stepnode list
                                            count=0
                                            for each_step_result in stepnote:
                                                if 'result' in each_step_result:
                                                    count+=1
                                            print 'Executed steps number in scripts is',count
                                            # get the test steps number in tcsteps list

                                            counta=0
                                            for each_step in tcsteps:
                                                if 'step_number' in each_step:
                                                    counta += 1
                                            print 'Steps number in the TestCase ' + TC_Name +' is ',counta

                                            if count==counta:
                                                #the result matches step number
                                                steplog=''
                                                i = 1
                                                durationflag = False

                                                for log in stepnote:
                                                    # TC_execution duration equals the all steps duration sum
                                                    # step end time minus start time equals each step duration
                                                    if durationflag == False:
                                                        starttime = datetime.datetime.strptime(log[0:19], '%Y-%m-%d %H:%M:%S')
                                                        endtime = datetime.datetime.strptime(log[0:19], '%Y-%m-%d %H:%M:%S')
                                                        # print 'this is start time'
                                                        # print starttime


                                                    if 'result' not in log:
                                                        steplog+=log
                                                        durationflag = True  # this step is not done yet.
                                                    else:
                                                        each_step_result=log[-3:-2]
                                                        # print 'this is step log'
                                                        # print steplog

                                                        TC_Result_Steps.append(
                                                            {'step_number': str(i), 'result': each_step_result,
                                                             'notes': steplog})
                                                        i += 1
                                                        steplog=''

                                                        endtime = datetime.datetime.strptime(log[0:19], '%Y-%m-%d %H:%M:%S')

                                                        delta = endtime - starttime
                                                        # print 'delta', delta

                                                        TC_execution_duration = delta

                                                # print 'this is tc result steps'
                                                # print TC_Result_Steps
                                                #
                                                # print 'this is tc execution time'
                                                # print TC_execution_duration

                                                # update test result remotely using API
                                                # Nov 9, 2016
                                                # determine the execution build name

                                                # if 'Win' in Platform_Name:
                                                #     buildname = TC_build_name_WIN
                                                # else:
                                                #     buildname = TC_build_name_MAC
                                                # the builds info is as following
                                                # [{'name': '4.00.0000.06', 'notes': '', 'testplan_id': '557', 'closed_on_date': '', 'release_date': '', 'is_open': '1', 'active': '1', 'creation_ts': '2016-11-25 10:16:46', 'id': '20'}, {'name': '4.02.0000.01', 'notes': '', 'testplan_id': '557', 'closed_on_date': '', 'release_date': '', 'is_open': '1', 'active': '1', 'creation_ts': '2016-11-25 11:16:59', 'id': '21'}]
                                                buildnamelist = tls.getBuildsForTestPlan(testplan['id'])
                                                buildname = buildnamelist[0]['name']

                                                # determine the test final result
                                                # get information from TC_Result_Steps
                                                for each_step_result in TC_Result_Steps:
                                                    # print 'this is each step result'

                                                    #print "each_step_result.get('result')", each_step_result.get('result')
                                                    if each_step_result.get('result') != 'p':
                                                        TC_Result = 'f'
                                                        break
                                                    else:
                                                        TC_Result = 'p'

                                                # update test result remotely using API
                                                # print 'TC_Result',TC_Result

                                                Update_timestamp=(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                                                duration_min=getduration(str(TC_execution_duration))



                                                getExecution=tls.reportTCResult(TC_Platform['tcase_id'], testplan['id'], buildname, TC_Result,
                                                                           'notes', guess=True,
                                                                           testcaseexternalid=TC_Platform['external_id'],
                                                                           platformname=TC_Platform['platform_name'],
                                                                           execduration=duration_min,
                                                                           timestamp=Update_timestamp, steps=TC_Result_Steps)
                                                # updated to testlink successfully.
                                                # 2016.11.21
                                                print TC_Name + " on " + Platform_Name + " under " + testplan['name'] + " of " + project['name'] +" has been updated to testlink."
                                                #  upload screenshot attachments if there's any mistake during the execution.
                                                ExecutionID=getExecution[0]['id']
                                                pngfiles=glob.glob(r'E:\TestLinkIntegration\*.png')

                                                if TC_Result == 'f':
                                                    for png in pngfiles:
                                                        tls.uploadExecutionAttachment(png,ExecutionID,'reference screenshot','reference screenshot')
                                                        print 'The '+png+ ' has been uploaded to testlink.'
                                                        os.remove(png)

                                                executed_number += 1
                                                if TC_Result == 'p':
                                                    executed_pass_number += 1
                                                else:
                                                    executed_fail_number += 1
                                            else:
                                                print 'something went wrong, no test result has been updated to testlink, which probably due to some steps error.'
                except:
                    pass
            print 'Total number test cases that were executed, failed number, pass number', executed_number, executed_fail_number, executed_pass_number















