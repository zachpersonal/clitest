# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from ssh_cmd import *
from to_log import *
from ssh_connect import ssh_conn
import random

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
# 测试 buzz
    buzzResult = SendCmd("buzz")
    if "Enabled   Status" in buzzResult:
        print "Pass buzz"
    else:
        print "Failed buzz"

# 测试 buzz -a list
    listResult = SendCmd("buzz -a list")
    if "Enabled   Status" in listResult:
        print "Pass buzz -a list"
    else:
        print "Failed buzz -a list"
# 测试 buzz enable buzz -a disable
    if "Yes" in listResult:
        SendCmd("buzz -a disable")
        disableResult = SendCmd("buzz")
        if "No" in disableResult:
            print "Pass buzz enable buzz -a disable"
# 测试 buzz disable buzz -a off
            disableOffResult = SendCmd("buzz -a off")
            if "" in disableOffResult:
                print "Pass buzz disable buzz -a off"
            else:
                print "Failed buzz disable buzz -a off"
        else:
            print "Failed buzz enable buzz -a disable"
# 测试 buzz disable buzz -a disable
        SendCmd("buzz -a disable")
        disableResult = SendCmd("buzz")
        if "No" in disableResult:
            print "Pass buzz disable buzz -a disable"
# 测试 buzz disable buzz -a on
            disableOnResult = SendCmd("buzz -a on")
            if "Buzzer is disabled" in disableOnResult:
                print "Pass buzz disable buzz -a on"
            else:
                print "Failed buzz disable buzz -a on"
        else:
            print "Failed buzz disable buzz -a disable"
# 测试 buzz disable buzz -a enable
    else:
        SendCmd("buzz -a enable")
        enableResult = SendCmd("buzz")
        if "Yes" in enableResult and "Silent" in enableResult:
            print "Pass buzz disable buzz -a enable"
# 测试 buzz enable off buzz -a off
            SendCmd("buzz -a off")
            enableOffOffResult = SendCmd("buzz")
            if "Yes" in enableOffOffResult and "Silent" in enableOffOffResult:
                print "Pass buzz enable off buzz -a off"
# 测试 buzz enable off buzz -a on
                SendCmd("buzz -a on")
                enableOffOnResult = SendCmd("buzz")
                if "Yes" in enableOffOnResult and "Sounding" in enableOffOnResult:
                    print "Pass buzz enable off buzz -a on"
# 测试 buzz enable on buzz -a on
                    SendCmd("buzz -a on")
                    enableOnOnResult = SendCmd("buzz")
                    if "Yes" in enableOnOnResult and "Sounding" in enableOnOnResult:
                        print "Pass buzz enable on buzz -a on"
                    else:
                        print "Failed buzz enable on buzz -a on"
                else:
                    print "Failed buzz enable off buzz -a on"
            else:
                print "Failed buzz enable off buzz -a off"

        else:
            print "Failed buzz disable buzz -a enable"
# 失败测试
    failedTest = SendCmd("buzz -i off")
    if "Invalid option for the command or the action" in failedTest:
        print "Pass buzz -i off"
    else:
        print "Failed buzz -i off"
    failedTest = SendCmd("buzz -a abc")
    if "Invalid setting parameters" in failedTest:
        print "Pass buzz -a abc"
    else:
        print "Failed buzz -a abc"
# 关闭buzz
    SendCmd("buzz -a off")
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped