# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
import random
import re
Pass = "'result': 'p'"
Fail = "'result': 'f'"
import string



def Verifyctrlv(c):

    ctrllist = list()

    data = SendCmd(c, "ctrl -v")
    ctrlinfoall = data.split("-------------------------------------------------------------------------------\r\n")
    ctrlinfo = ctrlinfoall[1:]
    '''
CtrlId: 2                               Alias: test
OperationalStatus: OK                   PowerOnTime: 7 hours 42 minutes
ControllerRole: Primary                 ReadinessStatus: Active
LUNAffinity: Disabled                   LunmappingMethod: Name Based
CacheUsagePercentage: 0                 DirtyCachePercentage: 0
PartNo: F29000020000177                 SerialNo: MA6D16508700019
HWRev: B1                               WWN: 2101-0001-555b-b258
CmdProtocol: SCSI-3                     ALUA: Disabled
MemType0: DDR4 SDRAM  (Slot 0)          MemSize0:   8 GB  (Slot 0)
MemType1: DDR4 SDRAM  (Slot 1)          MemSize1:   8 GB  (Slot 1)
MemType2:        N/A  (Slot 2)          MemSize2:    N/A  (Slot 2)
MemType3:        N/A  (Slot 3)          MemSize3:    N/A  (Slot 3)
FlashType: Flash Memory                 FlashSize: 16 GB
NVRAMType: SRAM                         NVRAMSize: 1 MB
BootLoaderVersion: 15.26.0000.00        BootLoaderBuildDate: Dec 06, 2016
FirmwareVersion: 12.00.9999.82          FirmwareBuildDate: Apr 28, 2017
SoftwareVersion: 12.00.9999.82          SoftwareBuildDate: Apr 28, 2017
DiskArrayPresent: 2                     OverallRAIDStatus: OK
LogDrvPresent: 2                        LogDrvOnline: 2
LogDrvOffline: 0                        LogDrvCritical: 0
PhyDrvPresent: 10                       PhyDrvOnline: 7
PhyDrvOffline: 0                        PhyDrvPFA: 0
GlobalSparePresent: 2                   DedicatedSparePresent: 0
RevertibleGlobalSparePresent: 0         RevertibleDedicatedSparePresent: 0
RevertibleGlobalSpareUsed: 0            RevertibleDedicatedSpareUsed: 0
WriteThroughMode: 0                     MaxSectorSize: 4 KB
PreferredCacheLineSize: 64              CacheLineSize: 64
Coercion: Enabled                       CoercionMethod: GBTruncate
SMART: Enabled                          SMARTPollingInterval: 24 minutes
MigrationStorage: DDF                   CacheFlushInterval: 1
PollInterval: 80                        AdaptiveWBCache: Enabled
HostCacheFlushing: Enabled              ForcedReadAhead: Enabled
Battery: Enabled                        CommonWorld: Disabled
Liquid: Disabled                        DriveCmd: Enabled
PowerSavingIdleTime: 11 hours 22 minutes
PowerSavingStandbyTime: 11 hours 22 minutes
PowerSavingStoppedTime: 11 hours 22 minutes
PseudoDeviceType: CTRL                  PerfectRebuildAvailable: 64
VAAIsupport: Disabled                   SSDTrimSupport: Enabled
'''
    # keys=("CtrlId","Alias","OperationalStatus","PowerOnTime","ControllerRole","ReadinessStatus","LUNAffinity","LunmappingMethod"
    #       ,"CacheUsagePercentage","DirtyCachePercentage","PartNo","SerialNo","HWRev","WWN","CmdProtocol", "ALUA","MemType0","MemType1","MemType2","MemType3",
    #       "MemSize0","MemSize1","MemSize2","MemSize3","FlashType","FlashSize","NVRAMType","NVRAMSize","BootLoaderVersion","BootLoaderBuildDate","FirmwareVersion",
    #       "FirmwareBuildDate","SoftwareVersion","SoftwareBuildDate","DiskArrayPresent","OverallRAIDStatus","LogDrvPresent","LogDrvOnline","LogDrvOffline",
    #       "LogDrvCritical","LogDrvCritical","PhyDrvPresent","PhyDrvOnline","PhyDrvOffline","PhyDrvPFA","GlobalSparePresent","DedicatedSparePresent",
    #       "RevertibleGlobalSparePresent","RevertibleDedicatedSparePresent","RevertibleGlobalSpareUsed","RevertibleDedicatedSpareUsed","write_through_mode",
    #       "MaxSectorSize","PreferredCacheLineSize","CacheLineSize","Coercion","CoercionMethod","SMART","SMARTPollingInterval","MigrationStorage",
    #       "CacheFlushInterval","PollInterval","AdaptiveWBCache","HostCacheFlushing","ForcedReadAhead","Battery","CommonWorld","Liquid","DriveCmd",
    #       "PowerSavingIdleTime","PowerSavingStandbyTime","PowerSavingStoppedTime","PseudoDeviceType","PerfectRebuildAvailable","VAAIsupport","SSDTrimSupport")
    # keys = (
    #     "CtrlId", "Alias", "OperationalStatus", "PowerOnTime", "ControllerRole", "ReadinessStatus", "LUNAffinity",
    #     "LunmappingMethod"
    #     , "CacheUsagePercentage", "DirtyCachePercentage", "PartNo", "SerialNo", "HWRev", "WWN", "CmdProtocol", "ALUA",
    #     "MemType0", "MemType1", "MemType2", "MemType3",
    #     "MemSize0", "MemSize1", "MemSize2", "MemSize3", "FlashType", "FlashSize", "NVRAMType", "NVRAMSize",
    #     "BootLoaderVersion", "BootLoaderBuildDate", "FirmwareVersion",
    #     "FirmwareBuildDate", "SoftwareVersion", "SoftwareBuildDate", "DiskArrayPresent", "OverallRAIDStatus",
    #     "LogDrvPresent", "LogDrvOnline", "LogDrvOffline",
    #     "LogDrvCritical", "PhyDrvPresent", "PhyDrvOnline", "PhyDrvOffline", "PhyDrvPFA",
    #     "GlobalSparePresent", "DedicatedSparePresent",
    #     "RevertibleGlobalSparePresent", "RevertibleDedicatedSparePresent", "RevertibleGlobalSpareUsed",
    #     "RevertibleDedicatedSpareUsed", "write_through_mode",
    #     "MaxSectorSize", "PreferredCacheLineSize", "CacheLineSize", "Coercion", "CoercionMethod", "SMART",
    #     "SMARTPollingInterval", "MigrationStorage",
    #     "CacheFlushInterval", "PollInterval", "AdaptiveWBCache", "HostCacheFlushing", "ForcedReadAhead", "Battery",
    #     "CommonWorld", "Liquid", "DriveCmd",
    #     "PowerSavingIdleTime", "PowerSavingStandbyTime", "PowerSavingStoppedTime", "PseudoDeviceType",
    #     "PerfectRebuildAvailable", "VAAIsupport", "SSDTrimSupport")



    for data in ctrlinfo:
        datalist = data.replace("administrator@cli> ", "").split("\r\n")
        data = data.replace("\r\n", "").replace("administrator@cli>", "")
        keys=list()
        for eachdata in datalist:
            singledata=eachdata.split("         ")
            for each in singledata:
                each=each.rstrip()
                each =each.lstrip()
                slicenum=each.find(": ")
                if each!="":
                    keys.append(each[0:slicenum])

        i = 0
        ctrl = dict()
        for key in keys:

            if i < len(keys) - 1:
                # print key, (data.find(key) + len(key) + 2), (data.find(keys[i + 1]))
                ctrl[key] = data[(data.find(key) + len(key) + 2):(data.find(keys[i + 1]))].rstrip()
            else:
                ctrl[key] = data[(data.find(key) + len(key) + 2):].rstrip()
            i += 1

        ctrllist.append(ctrl)
        #print ctrllist

    return ctrllist


def verifyCtrl(c):
    FailFlag = False
    tolog("verify ctrl")
    result = SendCmd(c, "ctrl")
    if "CtrlId        Alias        OperationalStatus        ReadinessStatus" not in result or "is Primary" not in result:
        FailFlag = True
        tolog("Fail: verify ctrl")
    for ctrlID in [1, 2]:
        tolog("verify ctrl -i "+str(ctrlID))
        result = SendCmd(c, "ctrl -i " + str(ctrlID))
        if "CtrlId        Alias        OperationalStatus        ReadinessStatus" not in result or str(ctrlID) not in result:
            FailFlag = True
            tolog("Fail:ctrl -i "+str(ctrlID))
    tolog("verify ctrl -i there is no ctrl ID")
    result = SendCmd(c, "ctrl -i 0")
    if "Error" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail: verify ctrl -i there is no ctrl ID")
    tolog("verify ctrl -i")
    result = SendCmd(c, "ctrl -i")
    if "Error" not in result or "Missing parameter" not in result:
        FailFlag = True
        tolog("Fail: ctrl -i")
    tolog("verify ctrl -x")
    result = SendCmd(c, "ctrl -x")
    if "Error" not in result or "Invalid option" not in result:
        FailFlag = True
        tolog("Fail: ctrl -x")
    tolog("verify ctrl abc")
    result = SendCmd(c, "ctrl abc")
    if "Error" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail: ctrl abc")
    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)
def verifyCtrlList(c):
    FailFlag = False
    tolog("verify ctrl list")
    tolog("verify ctrl -a list")
    result = SendCmd(c, "ctrl -a list")
    if "CtrlId        Alias        OperationalStatus        ReadinessStatus" not in result or "is Primary" not in result:
        FailFlag = True
        tolog("Fail: ctrl -a list")
    tolog("verify ctrl -a list -i the ctrl ID")
    for ctrlID in [1, 2]:
        tolog("verify ctrl -a list -i "+str(ctrlID))
        result = SendCmd(c, "ctrl -a list -i " + str(ctrlID))
        if "CtrlId        Alias        OperationalStatus        ReadinessStatus" not in result or str(ctrlID) not in result:
            FailFlag = True
            tolog("Fail:ctrl -a list -i "+str(ctrlID))
    tolog("verify ctrl -a list -i there is no ctrl ID")
    result = SendCmd(c, "ctrl -a list -i 3")
    if "Error" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail: verify ctrl -a list -i there is no ctrl ID")
    tolog("verify ctrl -a list -i")
    result = SendCmd(c, "ctrl -a list -i")
    if "Error" not in result or "Missing parameter" not in result:
        FailFlag = True
        tolog("Fail: verify ctrl -a list -i")
    tolog("verify ctrl -a abc")
    result = SendCmd(c, "ctrl -a abc")
    if "Error" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("verify ctrl -a abc")
    tolog("verify ctrl -a list -x 1")
    result = SendCmd(c, "ctrl -a list -x 1")
    if "Error" not in result or "Invalid option" not in result:
        FailFlag = True
        tolog("Fail: verify ctrl -a list -x 1")
    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)
def verifyCtrlV(c):
    FailFlag = False
    tolog("verify ctrl -v")
    result = SendCmd(c, "ctrl -v")
    if result.count(":") != 150:
        FailFlag = True
        tolog("Fail:ctrl -i ")
    for ctrlID in [1, 2]:
        tolog("verify ctrl -v -i "+str(ctrlID))
        result = SendCmd(c, "ctrl -v -i " + str(ctrlID))
        if result.count(":") != 75:
            FailFlag = True
            tolog("Fail:ctrl -i "+str(ctrlID))
    tolog("verify ctrl -v -i")
    result = SendCmd(c, "ctrl -v -i")
    if "Error" not in result or "Missing parameter" not in result:
        FailFlag = True
        tolog("Fail: ctrl -v -i")
    tolog("verify ctrl -v -x")
    result = SendCmd(c, "ctrl -v -x")
    if "Error" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail: ctrl -v -x")
    tolog("verify ctrl -v abc")
    result = SendCmd(c, "ctrl -v abc")
    if "Error" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail: ctrl -v abc")
    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)
def verifyCtrlListV(c):
    FailFlag = False
    tolog("verify ctrl -a list -v")
    result = SendCmd(c, "ctrl -a list -v")
    if result.count(":") != 150:
        FailFlag = True
        tolog("Fail:ctrl -a list -v")
    for ctrlID in [1, 2]:
        tolog("verify ctrl -a list -v -i "+str(ctrlID))
        result = SendCmd(c, "ctrl -a list -v -i " + str(ctrlID))
        if result.count(":") != 75:
            FailFlag = True
            tolog("ctrl -a list -v -i "+str(ctrlID))
    tolog("verify ctrl -a list -v -i")
    result = SendCmd(c, "ctrl -a list -v -i")
    if "Error" not in result or "Missing parameter" not in result:
        FailFlag = True
        tolog("Fail: ctrl -a list -v -i")
    tolog("verify ctrl -a list -v -x")
    result = SendCmd(c, "ctrl -a list -v -x")
    if "Error" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail: ctrl -a list -v -x")
    tolog("verify ctrl -a list -v abc")
    result = SendCmd(c, "ctrl -a list -v abc")
    if "Error" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail: ctrl -a list -v abc")
    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)
def verifyCtrlL(c):
    FailFlag = False
    tolog("verify ctrl -l")
    result = SendCmd(c, "ctrl -l")
    if "LocalCtrlId:" not in result:
        FailFlag = True
        tolog("Fail: verify ctrl -l")
    for ctrlID in [1, 2]:
        tolog("verify ctrl -l -i "+str(ctrlID))
        result = SendCmd(c, "ctrl -l -i "+str(ctrlID))
        if "LocalCtrlId:" not in result:
            FailFlag = True
            tolog("Fail: verify ctrl -l -i "+str(ctrlID))
    tolog("verify ctrl -l -i 4")
    result = SendCmd(c, "ctrl -l -i 4")
    if "Error" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail: verify ctrl -l -i 4")
    tolog("verify ctrl -l abc")
    result = SendCmd(c, "ctrl -l abc")
    if "Error" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail: verify ctrl -l abc")
    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)
def verifyCtrlClear(c):
    FailFlag = False
    for ctrlID in [1, 2]:
        tolog("verify ctrl -a clear -i "+str(ctrlID)+" -t watermark")
        result = SendCmd(c, "ctrl -a clear -i "+str(ctrlID)+" -t watermark")
        if "Error" in result or "ctrl -a clear -i "+str(ctrlID)+" -t watermark" not in result:
            FailFlag = True
            tolog("Fail: verify ctrl -a clear -i "+str(ctrlID)+" -t watermark")
    tolog("verify ctrl -a clear -t watermark")
    result = SendCmd(c, "ctrl -a clear -t watermark")
    if "Error" in result or "ctrl -a clear -t watermark" not in result:
        FailFlag = True
        tolog("Fail: ctrl -a clear -t watermark")
    for ctrlID in [1, 2]:
        tolog("verify ctrl -a clear -t watermark -i "+str(ctrlID))
        result = SendCmd(c, "ctrl -a clear -t watermark -i "+str(ctrlID))
        if "Error" in result or "ctrl -a clear -t watermark -i "+str(ctrlID) not in result:
            FailFlag = True
            tolog("Fail: verify ctrl -a clear -t watermark -i "+str(ctrlID))
    tolog("verify ctrl -a clear -i there is no ctrl's ID -t watermark")
    result = SendCmd(c, "ctrl -a clear -i 3 -t watermark")
    if "Error" not in result:
        FailFlag = True
        tolog("Fail: verify ctrl -a clear -i there is no ctrl's ID -t watermark")
    tolog("verify ctrl -a clear -i ctrl's ID")
    result = SendCmd(c, "ctrl -a clear -i 1")
    if "Error" not in result or "Missing parameter" not in result:
        FailFlag = True
        tolog("Fail: verify ctrl -a clear -i ctrl's ID")
    tolog("verify ctrl -a clear -i ctrl's ID -t abc")
    result = SendCmd(c, "ctrl -a clear -i 2 -t abc")
    if "Error" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog("Fail: ctrl -a clear -i ctrl's ID -t abc")
    tolog("verify ctrl -a clear -x")
    result = SendCmd(c, "ctrl -a clear -x")
    if "Error" not in result or "Invalid option" not in result:
        FailFlag = True
        tolog("Fail: ctrl -a clear -x")
    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)
def verifyCtrlMod(c):
    FailFlag = False
    tolog("verify ctrl -a mod")
    result = SendCmd(c, "ctrl")
    for index in [4, 5]:
        row = result.split("\r\n")[index]
        if row.split()[-2] == "OK":
            CtrlID = row.split()[0]
            tolog("verify ctrl -a mod -i " + str(CtrlID) + " -s <list of settings>")

            # verify alias
            for values in ['test_12', '12_test', 'test 12', '_', '123', 'test']:
                result = SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + " -s " + '"alias = ' + values + '"')
                result = SendCmd(c, "ctrl -v -i " + str(CtrlID))
                if "Alias: " + values not in result:
                    FailFlag = True
                    tolog("Fail: " + "ctrl -a mod -i " + str(CtrlID) + " -s alias = " + values + '"')

            # verify the values of enable or disable
            for values in ['disable', 'enable']:
                option = ["SMART = " + values,
                          "AdaptiveWBCache = " + values,
                          "HostCacheFlushing = " + values,
                          "ForcedReadAhead = " + values,
                          "SSDTrimSupport = " + values,
                          # "VAAIsupport = " + values,
                          "Coercion = " + values,
                          # to be confirmed
                          "Coercion = enable"
                          ]
                for Op in option:
                    SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + " -s " + '"' + Op + '"')
                    result = SendCmd(c, "ctrl -v -i " + str(CtrlID))
                    if Op.split()[0] + ': ' + Op.split()[-1].capitalize() + 'd' not in result:
                        FailFlag = True
                        tolog("Fail: " + "ctrl -a mod -s " + '"' + Op + '"')

            # verify the values of times option -- boundary value testing
            for option in ["powersavingidletime", "powersavingstandbytime", "powersavingstoppedtime"]:
                for values in [0, 1, 1439, 1440]:
                    # print "ctrl -a mod -i " + str(CtrlID) + " -s " + '"' + option + " = " + str(values) + '"'
                    result = SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + " -s " + '"' + option + " = " + str(values) + '"')
                    if "Error" in result:
                        FailFlag = True
                        tolog("Fail:" + "ctrl -a mod -i " + str(CtrlID) + " -s " + '"' + option + " = " + str(values) + '"')

            # Failed the test
            for values in ['123']:
                option = ["SMART = " + values,
                          "AdaptiveWBCache = " + values,
                          "HostCacheFlushing = " + values,
                          "ForcedReadAhead = " + values,
                          "SSDTrimSupport = " + values,
                          # "VAAIsupport = " + values,
                          "Coercion = " + values,
                          ]
                for Op in option:
                    SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + " -s " + '"' + Op + '"')
                    result = SendCmd(c, "ctrl -v -i " + str(CtrlID))
                    if "Error" not in result or "Invalid setting parameters" not in result:
                        FailFlag = True
                        tolog("Fail: ctrl -a mod -i " + str(CtrlID) + " -s " + '"' + Op + '"')

            for option in ["powersavingidletime", "powersavingstandbytime", "powersavingstoppedtime"]:
                for values in [-1, 1441]:
                    # print "ctrl -a mod -i " + str(CtrlID) + " -s " + '"' + option + " = " + str(values) + '"'
                    result = SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + " -s " + '"' + option + " = " + str(values) + '"')
                    if "Error" not in result or "Invalid setting parameters" not in result:
                        FailFlag = True
                        tolog("Fail:" + "ctrl -a mod -i " + str(CtrlID) + " -s " + '"' + option + " = " + str(values) + '"')

            for values in ['  ', 'aaaa1aaaa2aaaa3aaaa4aaaa5aaaa6aaaa7aaaa8aaaa9aaaa']:
                result = SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + " -s " + '"alias = ' + values + '"')
                if "Error" not in result:
                    FailFlag = True
                    tolog("Fail: " + "ctrl -a mod -i " + str(CtrlID) + " -s alias = " + values + '"')

            result = SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + " -x ")
            if "Error" not in result or "Invalid option" not in result:
                FailFlag = True
                tolog("Fail: ctrl -a mod -i " + str(CtrlID) + " -x ")

            result = SendCmd(c, "ctrl -a mod -i 3 -s " + '"alias = test"')
            if "Error" not in result or "Invalid setting parameters" not in result:
                FailFlag =True
                tolog("Fail: ctrl -a mod -i 3 -s " + '"alias = test"')
    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)
if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyCtrl(c)
    verifyCtrlList(c)
    verifyCtrlV(c)
    verifyCtrlListV(c)
    verifyCtrlL(c)
    verifyCtrlMod(c)
    verifyCtrlClear(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped