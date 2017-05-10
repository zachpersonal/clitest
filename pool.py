# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
import random
maxnamelength=25

Pass = "'result': 'p'"
Fail = "'result': 'f'"
Failprompt="Failed on verifying "
# added on March 10th, 2017
# this global setting will set how many volumes, snapshots and clones to be created in the test env.
# volsnapshotclonenumbers=10
# added on March 10th, 2017
# this global setting will set how many pool(s) to be created. if ==0, then the script will
# create the largest number pools according to the available physical drives.
#   if ==1:
#     if physcal drives ==2: create 1 pool  - no available pd
#     if physcal drives=3: create 1 raid1 pool - 1 available pd
#     if physcal drives=4: create 1 raid5 pool - 1 available pd
#     if physcal drives>=5: create 1 raid5/6 pool - 1 or 2 available pds
#   if ==2:
#      create pool using all phydrvs

poolnumber=[0,1,2]

class infodict:
    def __init__(self, name):
        self._name = name

    def getobject(self):

        result=SendCmd(c,self._name)

        infolist = list()
        data = list()
        data = result.split("\r\n")
        originaltab = data[2]
        tabtmp = data[2].split(" ")
        table = list()
        # the first column of the table will be the key in the dict


        for eachtab in tabtmp:
            if eachtab != "":
                table.append(eachtab.rstrip())
        data = data[4:-1]
        lentab = len(table) - 2
        Outinfo = dict()
        Outinfo = dict()

        for info in data:

            i = 0
            infolist = list()
            for i in range(lentab):
                # print originaltab.find(table[i + 2]), table[i + 1]
                infolist.append(info[originaltab.find(table[i + 1]):originaltab.find(table[i + 2]) - 1].rstrip())
                if i == lentab - 1:
                    infolist.append(info[originaltab.find(table[i + 2]):- 1].rstrip())

            Outinfo[info.split(" ")[0]] = infolist

        return Outinfo

def getpdlist(c):
    result = ""

    tolog("Get pd list:")

    result = SendCmd(c, "phydrv")
    pddict={}
#     administrator@cli> phydrv
# ===============================================================================
# PdId Model       Type    CfgCapacity Location     OpStatus ConfigStatus
# ===============================================================================
# 1    ST373455SS  SAS HDD 73 GB       Encl1 Slot1  OK       Pool0
# 3    HGST        SAS HDD 4 TB        Encl1 Slot3  OK       Pool0
# 4    ST3500418AS SAS HDD 499 GB      Encl1 Slot4  OK       Pool1
# 5    HGST        SAS HDD 4 TB        Encl1 Slot5  OK       Pool1
# 6    ST3146356SS SAS HDD 146 GB      Encl1 Slot6  OK       Pool2
# 7    ST3146356SS SAS HDD 146 GB      Encl1 Slot7  OK       Pool2
# 8    ST336754SS  SAS HDD 36 GB       Encl1 Slot8  OK       Pool3
# 9    HGST        SAS HDD 4 TB        Encl1 Slot9  OK       Pool3
# 10   ST3146356SS SAS HDD 146 GB      Encl1 Slot10 OK       Unconfigured
# 11   ST373455SS  SAS HDD 73 GB       Encl1 Slot11 OK       Unconfigured
# 12   HGST        SAS HDD 4 TB        Encl1 Slot12 OK       Unconfigured
    # pddict = {"1": ("HGST", "SAS HDD", "4 TB", "Encl1 Slot1", "OK", "Pool1")}
    infolist=list()
    pddata=list()

    pddata=result.split("\r\n")

    pdtab=pddata[2]
    # build 62 changed the output
    # modified on April 6th
    pddata=pddata[4:-1]
    # print  pddata
    for pdinfo in pddata:
        pddict[pdinfo[0:(pdtab.find("Model")-1)].rstrip()]=(pdinfo[pdtab.find("Model"):(pdtab.find("Type")-1)].rstrip(),pdinfo[pdtab.find("Type"):(pdtab.find("CfgCapacity")-1)].rstrip(),
                                                   pdinfo[pdtab.find("CfgCapacity"):(pdtab.find("Location") - 1)].rstrip(),pdinfo[pdtab.find("Location"):(pdtab.find("OpStatus") - 1)].rstrip(),
        pdinfo[pdtab.find("OpStatus"):(pdtab.find("ConfigStatus") - 1)].rstrip(),pdinfo[pdtab.find("ConfigStatus"):].rstrip())
    return pddict

'''
administrator@cli> phydrv
===============================================================================
PdId Model         Type CfgCapacity Location     OpStatus ConfigStatus
===============================================================================
1    HGST          SAS  4 TB        Encl1 Slot1  OK       Pool1
2    HUA723020ALA6 SAS  2 TB        Encl1 Slot2  OK       Pool1
3    HUA723020ALA6 SAS  2 TB        Encl1 Slot3  OK       Pool1
4    HUA723020ALA6 SAS  2 TB        Encl1 Slot4  OK       Pool1
5    HGST          SAS  4 TB        Encl1 Slot5  OK       Unconfigured
6    HGST          SAS  4 TB        Encl1 Slot6  OK       Revert Global
7    HGST          SAS  4 TB        Encl1 Slot7  OK       Unconfigured
25   SanDisk       SAS  31 GB       Encl1 Slot25 OK       Unconfigured
26   SanDisk       SAS  31 GB       Encl1 Slot26 OK       Unconfigured
27   SanDisk       SAS  31 GB       Encl1 Slot27 OK       Unconfigured
28   SanDisk       SAS  31 GB       Encl1 Slot28 OK       Unconfigured
'''
#     check OpStatus - OK and ConfigStatus - Unconfigured


def getvolinfo(c):
    voldata = SendCmd(c, "volume")

# old output before 47 build
# administrator@cli> volume
# ================================================================================
# Id        Name                PoolId    Capacity  UsedCapacity   Status
# ================================================================================
# 1         he                  1         20 GB     8.19 KB        Un-export
# 2         hea                 1         20 GB     8.19 KB        Exported
# 3         heat                1         20 GB     8.19 KB        Exported
# output in build 48
# volume
# ===============================================================================
# Id   Name                   PoolId TotalCap    UsedCap     Status     OpStatus
# ===============================================================================
# 0    pool1_1                1      15 TB       16.38 KB    Exported   OK
# 1    pool1_2                1      728.46 TB   16.38 KB    Exported   OK
# 2    pool1_3                1      734.71 TB   16.38 KB    Exported   OK
# 3    pool1_4                1      897.78 TB   16.38 KB    Exported   OK
# 4    pool1_5                1      838.80 TB   16.38 KB    Exported   OK
# 5    pool1_6                1      678.21 TB   16.38 KB    Exported   OK
# 6    pool1_7                1      239.71 TB   16.38 KB    Exported   OK
# 7    pool1_8                1      918.10 TB   16.38 KB    Exported   OK
# 8    pool0_1                0      196.67 TB   16.38 KB    Exported   OK

    voldata = voldata.split("\r\n")
    voltab = voldata[2]
    voldata = voldata[4:-1]
    voldict={}
    for volinfo in voldata:
        voldict[volinfo[0:(voltab.find("Name") - 1)].rstrip()] = (
        volinfo[voltab.find("Name"):(voltab.find("PoolId") - 1)].rstrip(),
        volinfo[voltab.find("PoolId"):(voltab.find("TotalCap") - 1)].rstrip(),
        volinfo[voltab.find("TotalCap"):(voltab.find("UsedCap") - 1)].rstrip(),
        volinfo[voltab.find("UsedCap"):(voltab.find("Status") - 1)].rstrip(),
        volinfo[voltab.find("Status"):(voltab.find("OpStatus") - 1)].rstrip(),
        volinfo[voltab.find("OpStatus"):].rstrip())

    return voldict

def getavailpd(c):
#     administrator@cli> phydrv
# ===============================================================================
# PdId  Model        Type  CfgCapacity  Location      OpStatus  ConfigStatus
# ===============================================================================
# 1     ST373455SS   SAS   73 GB        Encl1 Slot1   OK        Unconfigured
# 3     HGST         SAS   4 TB         Encl1 Slot3   OK        Unconfigured
# 4     ST3500418AS  SAS   499 GB       Encl1 Slot4   OK        Unconfigured
# 5     HGST         SAS   4 TB         Encl1 Slot5   OK        Unconfigured
# 6     ST3146356SS  SAS   146 GB       Encl1 Slot6   OK        Unconfigured
# 7     ST3146356SS  SAS   146 GB       Encl1 Slot7   OK        Unconfigured
# 8     ST336754SS   SAS   36 GB        Encl1 Slot8   OK        Unconfigured
# 9     HGST         SAS   4 TB         Encl1 Slot9   OK        Unconfigured
# 10    ST3146356SS  SAS   146 GB       Encl1 Slot10  OK        Unconfigured
# 11    ST373455SS   SAS   73 GB        Encl1 Slot11  OK        Unconfigured
# 12    HGST         SAS   4 TB         Encl1 Slot12  OK        Unconfigured
    pddict=getpdlist(c)
    pdhddlist=list()
    pdssdlist=list()
    # HDD and SSD cannot be mixed used in a pool, so return two list for HDD and SSD seperately.
    for key,value in pddict.items():
        if ("Unconfigured" in value[-1]) and value[-2]=="OK":
            if "SSD" in value[1]:
                pdssdlist.append(int(key))
            else:
                pdhddlist.append(int(key))


    pdhddlist.sort()
    pdssdlist.sort()
    return pdhddlist,pdssdlist


def poolcleanup(c):
    # March 15, 2017
    # it will remove pool, volume, snapshot/clone if there's any.

    pddict = getpdlist(c)
    poollist = list()

    for key, value in pddict.items():
        if "Pool" in value[-1]:
            # create pool id list
            if value[-1].split(" ")[0][4:] not in poollist:
                poollist.append(value[-1].split(" ")[0][4:])

    resp = ""
    if poollist:
        for eachpool in poollist:
            resp = SendCmd(c, "pool -a del -i " + eachpool)
            while "Can\'t delete Pool due to there exists derivatives" in resp:
                # remove forcefully if possible
                voldict = getvolinfo(c)

                for volkey, volvalue in voldict.items():

                    if volvalue[1] == eachpool:
                        volresp = SendCmd(c, "volume -a del -i " + volkey)
                        while "Fail to delete Volume" in volresp:
                            snapinfo = SendCmd(c, "volume -v -i " + volkey)
                            snapshotslist = (snapinfo.split("Snapshots: ", 1)[1].split("\r\n")[0]).split(", ")
                            for eachsnapshot in snapshotslist:
                                snapresp = SendCmd(c, "snapshot -a del -i " + eachsnapshot)
                                while "Fail to delete Snapshot" in snapresp:
                                    cloneinfo = SendCmd(c, "snapshot -v -i " + eachsnapshot)
                                    cloneslist = (cloneinfo.split("Clones: ", 1)[1].split("\r\n")[0]).split(", ")
                                    for eachclone in cloneslist:
                                        cloneresult = SendCmd(c, "clone -a del -i " + eachclone)
                                        if not (
                                                    "Error" in cloneresult or "Invalid" in cloneresult or "Fail" in cloneresult):
                                            tolog("Clone " + eachclone + " is deleted successfully.")
                                    snapresp = SendCmd(c, "snapshot -a del -i " + eachsnapshot)
                            volresp = SendCmd(c, "volume -a del -i " + volkey)
                resp = SendCmd(c, "pool -a del -i " + eachpool)


# Returns a random alphanumeric string of length 'length'
def random_key(length):
    import random
    import string
    key = ''
    for i in range(length):
        key += random.choice(string.lowercase + string.uppercase + string.digits+"_")
        #key += random.choice(string.lowercase + string.digits)
    return key

def createpoolpd(c,aliasname,raidlevel,stripesize,sectorsize,pdlist):
    # added stripe and sector on March 15, 2017
    stripelst = ["64kb", "128kb","256kb","512kb","1mb","64Kb","64kB","64KB","128Kb","128KB","128kB","256Kb","256KB","256kB","512Kb","512KB","512kB","1Mb","1MB","1mB"]
    #sectorlst = ["512b", "1kb", "2kb", "4kb","512B", "1Kb", "2Kb", "4Kb","1KB", "2KB", "4KB","1kB", "2kB", "4kB"]
    sectorlst = ["512b", "1kb", "2kb",  "512B", "1Kb", "2Kb", "1KB", "2KB", "1kB", "2kB"]
    if stripesize=="":
        stripesize=random.choice(stripelst)

    if sectorsize=="":
        sectorsize=random.choice(sectorlst)
    # will remove lower() once the new code is checked in to fix this issue.
    settings="name=" + aliasname + ",raid=" + raidlevel +", stripe="+stripesize.lower()+", sector="+sectorsize.lower()

    SendCmd(c,"pool -a add -s " +"\""+settings+"\""+ " -p " + pdlist)

def getpoolinfo(c):

    pooldata = SendCmd(c, "pool")

    # administrator@cli> pool
    # ===============================================================================
    # Id    Name    Status    TotalCapacity    UsedCapacity    FreeCapacity
    # ===============================================================================
    # 1     11      OK        72.48 GB         69.63 KB        72.48 GB
    # ===============================================================================
    # Id   Name                             OpStatus  TotalCap  UsedCap   FreeCap
    # ===============================================================================
    # 0    pp                               OK        72.48 GB  68.10 KB  72.48 GB
    pooldata = pooldata.split("\r\n")
    pooltab = pooldata[2]
    pooldata = pooldata[4:-1]
    pooldict = {}
    for poolinfo in pooldata:
        pooldict[poolinfo[0:(pooltab.find("Name") - 1)].rstrip()] = (
            poolinfo[pooltab.find("Name"):(pooltab.find("OpStatus") - 1)].rstrip(),
            poolinfo[pooltab.find("OpStatus"):(pooltab.find("TotalCap") - 1)].rstrip(),
            poolinfo[pooltab.find("TotalCap"):(pooltab.find("UsedCap") - 1)].rstrip(),
            poolinfo[pooltab.find("UsedCap"):(pooltab.find("FreeCap") - 1)].rstrip(),
            poolinfo[pooltab.find("FreeCap"):-1].rstrip())


    return pooldict


def getsnapshotinfo(c):
#     administrator@cli> snapshot
# ================================================================================
# Id    Name    PoolId Type        SourceId  UsedCapacity   Status
# ================================================================================
# 42    fdsdfa   1      volume      41        0 Byte         Un-export

# administrator@cli> snapshot
# ===============================================================================
# Id   Name              Type       SrcId UsedCap    Status    OpStatus
# ===============================================================================
# 0    test              volume     0     0 Byte     Un-Export OK
    snapshotdata = SendCmd(c, "snapshot")
    snapshotdata = snapshotdata.split("\r\n")
    snapshottab = snapshotdata[2]
    snapshotdata = snapshotdata[4:-1]
    snapshotdict = {}
    for snapshotinfo in snapshotdata:
        snapshotdict[snapshotinfo[0:(snapshottab.find("Name") - 1)].rstrip()] = (
            snapshotinfo[snapshottab.find("Name"):(snapshottab.find("Type") - 1)].rstrip(),
            snapshotinfo[snapshottab.find("Type"):(snapshottab.find("SrcId") - 1)].rstrip(),
            snapshotinfo[snapshottab.find("SrcId"):(snapshottab.find("UsedCap") - 1)].rstrip(),
            snapshotinfo[snapshottab.find("UsedCap"):(snapshottab.find("Status") - 1)].rstrip(),
            snapshotinfo[snapshottab.find("Status"):(snapshottab.find("OpStatus") - 1)].rstrip(),
            snapshotinfo[snapshottab.find("OpStatus"):].rstrip())

    return snapshotdict

def getscloneinfo(c):

# administrator@cli> clone
# ================================================================================
# Id   Name      Type      SourceId    TotalCapacity   UsedCapacity    Status
# ================================================================================
# 43   eefa      volume    42          100 GB          1.02 KB         Un-export

    clonedata = SendCmd(c, "clone")
    clonedata = clonedata.split("\r\n")
    clonetab = clonedata[2]
    clonedata = clonedata[4:-1]
    clonedict = {}
    for cloneinfo in clonedata:
        clonedict[cloneinfo[0:(clonetab.find("Name") - 1)].rstrip()] = (
            cloneinfo[clonetab.find("Name"):(clonetab.find("Type") - 1)].rstrip(),
            cloneinfo[clonetab.find("Type"):(clonetab.find("SourceId") - 1)].rstrip(),
            cloneinfo[clonetab.find("SourceId"):(clonetab.find("TotalCapacity") - 1)].rstrip(),
            cloneinfo[clonetab.find("TotalCapacity"):(clonetab.find("UsedCapacity") - 1)].rstrip(),
            cloneinfo[clonetab.find("UsedCapacity"):(clonetab.find("Status") - 1)].rstrip())

    return clonedict

def getscloneinfo(c):

# administrator@cli> clone
# ================================================================================
# Id   Name      Type      SourceId    TotalCapacity   UsedCapacity    Status
# ================================================================================
# 43   eefa      volume    42          100 GB          1.02 KB         Un-export

    clonedata = SendCmd(c, "clone")
    clonedata = clonedata.split("\r\n")
    clonetab = clonedata[2]
    clonedata = clonedata[4:-1]
    clonedict = {}
    for cloneinfo in clonedata:
        clonedict[cloneinfo[0:(clonetab.find("Name") - 1)].rstrip()] = (
            cloneinfo[clonetab.find("Name"):(clonetab.find("Type") - 1)].rstrip(),
            cloneinfo[clonetab.find("Type"):(clonetab.find("SourceId") - 1)].rstrip(),
            cloneinfo[clonetab.find("SourceId"):(clonetab.find("TotalCapacity") - 1)].rstrip(),
            cloneinfo[clonetab.find("TotalCapacity"):(clonetab.find("UsedCapacity") - 1)].rstrip(),
            cloneinfo[clonetab.find("UsedCapacity"):(clonetab.find("Status") - 1)].rstrip())

    return clonedict



def poolcreateandlist(c,poolnum):
    # list pool from 0 to physical maximum
    # List pool status with correct options pool, pool -a list, pool -v
    # List pool status with invalid options
    FailFlag=False
    # March 15, 2017
    # added hdd and ssd type condition
    poolforceclean(c)

    pdhddssdlist = getavailpd(c)
    poolnum=int(poolnum)
    for pdlist in pdhddssdlist:

        phydrvnum = len(pdlist)
        poolcount = 0
        if phydrvnum == 0:
            continue

            # from 1 pool to maximum
            # administrator@cli> pool
            # ===============================================================================
            # Id    Name    Status    TotalCapacity    UsedCapacity    FreeCapacity
            # ===============================================================================
            # 1     11      OK        72.48 GB         69.63 KB        72.48 GB
        if phydrvnum == 1:
            tolog("Only one phydrv is in the system, so no pool will be created.")
        if phydrvnum == 2:
            tolog("Two phydrvs are in the system, only raid 1 level pool will be created.")
            poolname = random_key(maxnamelength) + str(phydrvnum)
            createpoolpd(c, poolname, "1", "", "", str(pdlist[0]) + "," + str(pdlist[1]))
            poolcount += 1
            poolres = SendCmd(c, "pool"), SendCmd(c, "pool -a list")
            for eachres in poolres:
                if len(eachres.split("\r\n")) == poolcount + 5 and poolname in eachres:
                    if "-a list" in eachres:
                        tolog("pool -a list with phydrvum " + str(phydrvnum) + " succeeded.")
                    else:
                        tolog("pool with phydrvum " + str(phydrvnum) + " succeeded.")
                else:
                    FailFlag = True
                    tolog("Pool list with phydrvum " + str(phydrvnum) + "failed.")
                    break

        if phydrvnum == 3:
            if poolnum == 0 or poolnum == 2:
                tolog("Three phydrvs are in the system, only 1 raid 5 level pool will be created.")
                poolname = random_key(maxnamelength) + str(phydrvnum)
                createpoolpd(c, poolname, "5", "", "", str(pdlist).replace("[", "").replace("]", ""))
                poolcount += 1
                poolres = SendCmd(c, "pool"), SendCmd(c, "pool -a list")
                for eachres in poolres:
                    if len(eachres.split("\r\n")) == poolcount + 5 and poolname in eachres:
                        if "-a list" in eachres:
                            tolog("pool -a list with phydrvum " + str(phydrvnum) + "raid 5 succeeded.")
                        else:
                            tolog("pool with phydrvum " + str(phydrvnum) + "raid 5 succeeded.")
                    else:
                        FailFlag = True
                        tolog("Pool list with phydrvum " + str(phydrvnum) + " raid 5 failed.")
                        break
            else:
                tolog(
                    "Three phydrvs are in the system, only 1 raid 1 level pool will be created and 1 phydrv available.")
                poolname = random_key(maxnamelength) + str(phydrvnum - 1)
                # only the first two disks are used
                createpoolpd(c, poolname, "1", "", "", str(pdlist[0]) + "," + str(pdlist[1]))
                poolcount += 1
                poolres = SendCmd(c, "pool"), SendCmd(c, "pool -a list")
                for eachres in poolres:
                    if len(eachres.split("\r\n")) == poolcount + 5 and poolname in eachres:
                        if "-a list" in eachres:
                            tolog("pool -a list with phydrvum " + str(phydrvnum) + "raid 1 succeeded.")
                        else:
                            tolog("pool with phydrvum " + str(phydrvnum) + "raid 1 succeeded.")
                    else:
                        FailFlag = True
                        tolog("Pool list with phydrvum " + str(phydrvnum) + "raid 1 failed.")
                        break
        if phydrvnum == 4:

            if poolnum == 0:
                poolname = random_key(maxnamelength) + str(phydrvnum)

                tolog(str(phydrvnum) + " phydrvs are in the system, " + str(
                    phydrvnum / 2) + " raid 1 level pools will be created.")
                # pdstr = ' '.join(str(e) for e in pdlist)
                for i in range(1, phydrvnum + 1, 2):
                    createpoolpd(c, poolname + str(i / 2), "1", "", "",
                                 str(pdlist[(i - 1):(i + 1)]).replace("[", "").replace("]", "").replace(" ", ""))
                    poolcount += 1
                    # create volune in the pool

                poolres = SendCmd(c, "pool"), SendCmd(c, "pool -a list")
                for eachres in poolres:
                    if len(eachres.split("\r\n")) == poolcount + 5 and poolname in eachres:
                        if "-a list" in eachres:
                            tolog("pool -a list with phydrvum " + str(phydrvnum) + " succeeded.")
                        else:
                            tolog("pool with phydrvum " + str(phydrvnum) + " succeeded.")
                    else:
                        FailFlag = True
                        tolog("Pool list with phydrvum " + str(phydrvnum) + "failed.")
                        break
            if poolnum == 1:

                poolname = random_key(maxnamelength) + str(phydrvnum - 1)
                createpoolpd(c, poolname, "5", "", "", str(pdlist[0]) + "," + str(pdlist[1]) + "," + str(pdlist[2]))
                poolcount += 1
            if poolnum == 2:
                poolname = random_key(maxnamelength) + str(phydrvnum - 1)
                createpoolpd(c, poolname, "5", "", "",
                             str(pdlist[0]) + "," + str(pdlist[1]) + "," + str(pdlist[2]) + "," + str(pdlist[3]))
                poolcount += 1
        if phydrvnum >= 5:

            if poolnum == 0:
                if phydrvnum % 2 == 0:
                    poolname = random_key(maxnamelength) + str(phydrvnum)
                    tolog(str(phydrvnum) + " phydrvs are in the system, " + str(
                        phydrvnum / 2) + " raid 1 level pools will be created.")
                    # pdstr = ' '.join(str(e) for e in pdlist)
                    for i in range(1, phydrvnum + 1, 2):
                        createpoolpd(c, poolname + str(i / 2), "1", "", "",
                                     str(pdlist[(i - 1):(i + 1)]).replace("[", "").replace("]", "").replace(" ", ""))
                        poolcount += 1
                        # create volune in the pool

                    poolres = SendCmd(c, "pool"), SendCmd(c, "pool -a list")
                    SendCmd(c,"phydrv")
                    for eachres in poolres:
                        if len(eachres.split("\r\n")) == poolcount + 5 and poolname in eachres:
                            if "-a list" in eachres:
                                tolog("pool -a list with phydrvum " + str(phydrvnum) + " succeeded.")
                            else:
                                tolog("pool with phydrvum " + str(phydrvnum) + " succeeded.")
                        else:
                            FailFlag = True
                            tolog("Pool list with phydrvum " + str(phydrvnum) + "failed.")
                            break
                else:
                    poolname = random_key(maxnamelength) + str(phydrvnum)
                    tolog(str(phydrvnum) + " phydrvs are in the system, " + str(
                        phydrvnum / 2 - 1) + " raid 1 level pools " + " and 1 raid 5 level pool will be created.")
                    # pdstr = ' '.join(str(e) for e in pdlist)

                    for i in range(1, phydrvnum - 2, 2):
                        # pdids=pdstr[i - 1] + ","+pdstr[i]
                        createpoolpd(c, poolname + str(i / 2), "1", "", "",
                                     str(pdlist[(i - 1):(i + 1)]).replace("[", "").replace("]", "").replace(" ", ""))
                        # createpoolpd(c,poolname+str(i+1),"5",pdstr[phydrvnum-3]+","+pdstr[phydrvnum-2]+","+pdstr[phydrvnum-1])
                        poolcount += 1

                    createpoolpd(c, poolname + str(i), "5", "", "",
                                 str(pdlist[-3:]).replace("[", "").replace("]", "").replace(" ", ""))
                    poolcount += 1

                    poolres = SendCmd(c, "pool"), SendCmd(c, "pool -a list")
                    SendCmd(c, "phydrv")
                    for eachres in poolres:
                        if len(eachres.split("\r\n")) == poolcount + 5 and poolname in eachres:
                            if "-a list" in eachres:
                                tolog("pool -a list with phydrvum " + str(phydrvnum) + " succeeded.")
                            else:
                                tolog("pool with phydrvum " + str(phydrvnum) + " succeeded.")
                        else:
                            FailFlag = True
                            tolog("Pool list with phydrvum " + str(phydrvnum) + "failed.")
                            break
            if poolnum == 1:

                poolname = random_key(30) + "4"
                raidlevel = random.choice(["5", "6"])
                tolog(str(
                    phydrvnum) + " phydrvs are in the system, 1 raid 5 or raid 6 level pools will be created and " + str(
                    phydrvnum - 4) + " phydrvs are avalible.")
                createpoolpd(c, poolname, random.choice(["5", "6"]), "", "",
                             str(pdlist[0]) + "," + str(pdlist[1]) + "," + str(pdlist[2]) + "," + str(pdlist[3]))
                poolcount += 1
                poolres = SendCmd(c, "pool"), SendCmd(c, "pool -a list")
                SendCmd(c, "phydrv")
                for eachres in poolres:
                    if len(eachres.split("\r\n")) == poolcount + 5 and poolname in eachres:
                        if "-a list" in eachres:
                            tolog("pool -a list with phydrvum " + str(
                                phydrvnum) + " raid level" + raidlevel + " succeeded.")
                        else:
                            tolog("pool with phydrvum " + str(phydrvnum) + " raid level" + raidlevel + " succeeded.")
                    else:
                        FailFlag = True
                        tolog("Pool list with phydrvum " + str(phydrvnum) + " raid level" + raidlevel + " failed.")
                        break
            if poolnum == 2:
                poolname = random_key(maxnamelength) + str(phydrvnum)
                tolog(str(
                    phydrvnum) + " phydrvs are in the system, 1 raid 5 or raid 6 level pools will be created and no phydrv is avaible.")
                raidlevel = random.choice(["5", "6"])
                createpoolpd(c, poolname, raidlevel, "", "",
                             str(pdlist).replace("[", "").replace("]", "").replace(" ", ""))
                poolcount += 1
                poolres = SendCmd(c, "pool"), SendCmd(c, "pool -a list")
                SendCmd(c, "phydrv")
                for eachres in poolres:
                    if len(eachres.split("\r\n")) == poolcount + 5 and poolname in eachres:
                        if "-a list" in eachres:
                            tolog("pool -a list with phydrvum " + str(phydrvnum) + " raid " + raidlevel + " succeeded.")
                        else:
                            tolog("pool with phydrvum " + str(phydrvnum) + " raid " + raidlevel + " succeeded.")
                    else:
                        FailFlag = True
                        tolog("Pool list with phydrvum " + str(phydrvnum) + " raid " + raidlevel + " failed.")
                        break

    if FailFlag:

        tolog(Fail)

    else:
        tolog(Pass)


def bvtpoolcreateandlist(c, poolnum):
    # list pool from 0 to physical maximum
    # List pool status with correct options pool, pool -a list, pool -v
    # List pool status with invalid options
    FailFlag = False
    # March 15, 2017
    # added hdd and ssd type condition
    poolforceclean(c)

    pdhddssdlist = getavailpd(c)
    poolnum = int(poolnum)
    for pdlist in pdhddssdlist:

        phydrvnum = len(pdlist)
        poolcount = 0
        if phydrvnum == 0:
            continue

            # from 1 pool to maximum
            # administrator@cli> pool
            # ===============================================================================
            # Id    Name    Status    TotalCapacity    UsedCapacity    FreeCapacity
            # ===============================================================================
            # 1     11      OK        72.48 GB         69.63 KB        72.48 GB
        if phydrvnum == 1:
            tolog("Only one phydrv is in the system, so no pool will be created.")
        if phydrvnum == 2:
            tolog("Two phydrvs are in the system, only raid 1 level pool will be created.")
            poolname = random_key(maxnamelength) + str(phydrvnum)
            createpoolpd(c, poolname, "1", "", "", str(pdlist[0]) + "," + str(pdlist[1]))
            poolcount += 1
            poolres = SendCmd(c, "pool"), SendCmd(c, "pool -a list")
            for eachres in poolres:
                if len(eachres.split("\r\n")) == poolcount + 5 and poolname in eachres:
                    if "-a list" in eachres:
                        tolog("pool -a list with phydrvum " + str(phydrvnum) + " succeeded.")
                    else:
                        tolog("pool with phydrvum " + str(phydrvnum) + " succeeded.")
                else:
                    FailFlag = True
                    tolog("Pool list with phydrvum " + str(phydrvnum) + "failed.")
                    break

        if phydrvnum == 3:
            if poolnum == 0 or poolnum == 2:
                tolog("Three phydrvs are in the system, only 1 raid 5 level pool will be created.")
                poolname = random_key(maxnamelength) + str(phydrvnum)
                createpoolpd(c, poolname, "5", "", "", str(pdlist).replace("[", "").replace("]", ""))
                poolcount += 1
                poolres = SendCmd(c, "pool"), SendCmd(c, "pool -a list")
                for eachres in poolres:
                    if len(eachres.split("\r\n")) == poolcount + 5 and poolname in eachres:
                        if "-a list" in eachres:
                            tolog("pool -a list with phydrvum " + str(phydrvnum) + "raid 5 succeeded.")
                        else:
                            tolog("pool with phydrvum " + str(phydrvnum) + "raid 5 succeeded.")
                    else:
                        FailFlag = True
                        tolog("Pool list with phydrvum " + str(phydrvnum) + " raid 5 failed.")
                        break
            else:
                tolog(
                    "Three phydrvs are in the system, only 1 raid 1 level pool will be created and 1 phydrv available.")
                poolname = random_key(maxnamelength) + str(phydrvnum - 1)
                # only the first two disks are used
                createpoolpd(c, poolname, "1", "", "", str(pdlist[0]) + "," + str(pdlist[1]))
                poolcount += 1
                poolres = SendCmd(c, "pool"), SendCmd(c, "pool -a list")
                for eachres in poolres:
                    if len(eachres.split("\r\n")) == poolcount + 5 and poolname in eachres:
                        if "-a list" in eachres:
                            tolog("pool -a list with phydrvum " + str(phydrvnum) + "raid 1 succeeded.")
                        else:
                            tolog("pool with phydrvum " + str(phydrvnum) + "raid 1 succeeded.")
                    else:
                        FailFlag = True
                        tolog("Pool list with phydrvum " + str(phydrvnum) + "raid 1 failed.")
                        break
        if phydrvnum == 4:

            if poolnum == 0:
                poolname = random_key(maxnamelength) + str(phydrvnum)

                tolog(str(phydrvnum) + " phydrvs are in the system, " + str(
                    phydrvnum / 2) + " raid 1 level pools will be created.")
                # pdstr = ' '.join(str(e) for e in pdlist)
                for i in range(1, phydrvnum + 1, 2):
                    createpoolpd(c, poolname + str(i / 2), "1", "", "",
                                 str(pdlist[(i - 1):(i + 1)]).replace("[", "").replace("]", "").replace(" ", ""))
                    poolcount += 1
                    # create volune in the pool

                poolres = SendCmd(c, "pool"), SendCmd(c, "pool -a list")
                for eachres in poolres:
                    if len(eachres.split("\r\n")) == poolcount + 5 and poolname in eachres:
                        if "-a list" in eachres:
                            tolog("pool -a list with phydrvum " + str(phydrvnum) + " succeeded.")
                        else:
                            tolog("pool with phydrvum " + str(phydrvnum) + " succeeded.")
                    else:
                        FailFlag = True
                        tolog("Pool list with phydrvum " + str(phydrvnum) + "failed.")
                        break
            if poolnum == 1:
                poolname = random_key(maxnamelength) + str(phydrvnum - 1)
                createpoolpd(c, poolname, "5", "", "", str(pdlist[0]) + "," + str(pdlist[1]) + "," + str(pdlist[2]))
                poolcount += 1
            if poolnum == 2:
                poolname = random_key(maxnamelength) + str(phydrvnum - 1)
                createpoolpd(c, poolname, "5", "", "",
                             str(pdlist[0]) + "," + str(pdlist[1]) + "," + str(pdlist[2]) + "," + str(pdlist[3]))
                poolcount += 1
        if phydrvnum >= 5:

            if poolnum == 0:
                if phydrvnum % 2 == 0:
                    poolname = random_key(maxnamelength) + str(phydrvnum)
                    tolog(str(phydrvnum) + " phydrvs are in the system, " + str(
                        phydrvnum / 2) + " raid 1 level pools will be created.")
                    # pdstr = ' '.join(str(e) for e in pdlist)
                    for i in range(1, phydrvnum + 1, 2):
                        createpoolpd(c, poolname + str(i / 2), "1", "", "",
                                     str(pdlist[(i - 1):(i + 1)]).replace("[", "").replace("]", "").replace(" ", ""))
                        poolcount += 1
                        # create volune in the pool

                    poolres = SendCmd(c, "pool"), SendCmd(c, "pool -a list")
                    SendCmd(c, "phydrv")
                    for eachres in poolres:
                        if len(eachres.split("\r\n")) == poolcount + 5 and poolname in eachres:
                            if "-a list" in eachres:
                                tolog("pool -a list with phydrvum " + str(phydrvnum) + " succeeded.")
                            else:
                                tolog("pool with phydrvum " + str(phydrvnum) + " succeeded.")
                        else:
                            FailFlag = True
                            tolog("Pool list with phydrvum " + str(phydrvnum) + "failed.")
                            break
                else:
                    poolname = random_key(maxnamelength) + str(phydrvnum)
                    tolog(str(phydrvnum) + " phydrvs are in the system, " + str(
                        phydrvnum / 2 - 1) + " raid 1 level pools " + " and 1 raid 5 level pool will be created.")
                    # pdstr = ' '.join(str(e) for e in pdlist)

                    for i in range(1, phydrvnum - 2, 2):
                        # pdids=pdstr[i - 1] + ","+pdstr[i]
                        createpoolpd(c, poolname + str(i / 2), "1", "", "",
                                     str(pdlist[(i - 1):(i + 1)]).replace("[", "").replace("]", "").replace(" ", ""))
                        # createpoolpd(c,poolname+str(i+1),"5",pdstr[phydrvnum-3]+","+pdstr[phydrvnum-2]+","+pdstr[phydrvnum-1])
                        poolcount += 1

                    createpoolpd(c, poolname + str(i), "5", "", "",
                                 str(pdlist[-3:]).replace("[", "").replace("]", "").replace(" ", ""))
                    poolcount += 1

                    poolres = SendCmd(c, "pool"), SendCmd(c, "pool -a list")
                    SendCmd(c, "phydrv")
                    for eachres in poolres:
                        if len(eachres.split("\r\n")) == poolcount + 5 and poolname in eachres:
                            if "-a list" in eachres:
                                tolog("pool -a list with phydrvum " + str(phydrvnum) + " succeeded.")
                            else:
                                tolog("pool with phydrvum " + str(phydrvnum) + " succeeded.")
                        else:
                            FailFlag = True
                            tolog("Pool list with phydrvum " + str(phydrvnum) + "failed.")
                            break
            if poolnum == 1:

                poolname = random_key(30) + "4"
                raidlevel = random.choice(["5", "6"])
                tolog(str(
                    phydrvnum) + " phydrvs are in the system, 1 raid 5 or raid 6 level pools will be created and " + str(
                    phydrvnum - 4) + " phydrvs are avalible.")
                createpoolpd(c, poolname, random.choice(["5", "6"]), "", "",
                             str(pdlist[0]) + "," + str(pdlist[1]) + "," + str(pdlist[2]) + "," + str(pdlist[3]))
                poolcount += 1
                poolres = SendCmd(c, "pool"), SendCmd(c, "pool -a list")
                SendCmd(c, "phydrv")
                for eachres in poolres:
                    if len(eachres.split("\r\n")) == poolcount + 5 and poolname in eachres:
                        if "-a list" in eachres:
                            tolog("pool -a list with phydrvum " + str(
                                phydrvnum) + " raid level" + raidlevel + " succeeded.")
                        else:
                            tolog("pool with phydrvum " + str(phydrvnum) + " raid level" + raidlevel + " succeeded.")
                    else:
                        FailFlag = True
                        tolog("Pool list with phydrvum " + str(phydrvnum) + " raid level" + raidlevel + " failed.")
                        break
            if poolnum == 2:
                poolname = random_key(maxnamelength) + str(phydrvnum)
                tolog(str(
                    phydrvnum) + " phydrvs are in the system, 1 raid 5 or raid 6 level pools will be created and no phydrv is avaible.")
                raidlevel = random.choice(["5", "6"])
                createpoolpd(c, poolname, raidlevel, "", "",
                             str(pdlist).replace("[", "").replace("]", "").replace(" ", ""))
                poolcount += 1
                poolres = SendCmd(c, "pool"), SendCmd(c, "pool -a list")
                SendCmd(c, "phydrv")
                for eachres in poolres:
                    if len(eachres.split("\r\n")) == poolcount + 5 and poolname in eachres:
                        if "-a list" in eachres:
                            tolog("pool -a list with phydrvum " + str(phydrvnum) + " raid " + raidlevel + " succeeded.")
                        else:
                            tolog("pool with phydrvum " + str(phydrvnum) + " raid " + raidlevel + " succeeded.")
                    else:
                        FailFlag = True
                        tolog("Pool list with phydrvum " + str(phydrvnum) + " raid " + raidlevel + " failed.")
                        break

    return FailFlag


def volumecreate(c, poolid, name, capacity, blocksize, sectorsize):
    blocksizelst=["512b", "1kb", "2kb", "4kb", "8kb", "16kb", "32kb", "64kb","128kb"]
    sectorsizelst=["512b", "1kb", "2kb","4kb"]
    mincapacity=16
    maxcapacity=1000000

    if blocksize=="":
        blocksize=random.choice(blocksizelst)
    if sectorsize=="":
        sectorsize=random.choice(sectorsizelst)
    if capacity=="":
        capacity=random.randint(mincapacity, maxcapacity)

    settings ="name="+name+", capacity="+str(capacity)+"GB"+", block="+blocksize+", sector="+sectorsize
    # settings = "name=" + name + ", capacity=" + str(capacity) + "GB"
    SendCmd(c,"volume -a add -p "+poolid+" -s "+"\""+settings+"\"")

def volumecreateandlist(c,volnum):
    i=0
    j=0
    count=0
    FailFlag=False
    volnum=int(volnum)
    # tolog("I am here")
    pooldct=getpoolinfo(c)
    # administrator@cli> pool
    # ===============================================================================
    # Id    Name    Status    TotalCapacity    UsedCapacity    FreeCapacity
    # ===============================================================================
    # 1     11      OK        72.48 GB         69.63 KB        72.48 GB
    for poolid,poolvalue in pooldct.items():
        if (poolvalue[1]=="OK") or (poolvalue[1]=="OK, Synch") and float(poolvalue[-1].split(" ")[0])<=float(poolvalue[-3].split(" ")[0]):
            for i in range(1,volnum+1):
                volumecreate(c,poolid,"pool"+random_key(3)+poolid+"_"+str(i),"","","")
                # volumecreate(c, poolid, "pool" + poolid + "_" + str(i), "")
                count+=1
                # tolog("I am here2")
        j+=1
    res=SendCmd(c,"volume")
    # tolog("I am here 3")
    if i==0:
        tolog("No volume exists")
    else:
        if len(res.split("\r\n")) ==  count+ 5 and str(count-1) in res:
            tolog("Volumes are created succesfully.")
        else:
            FailFlag=True
            tolog("Volumes are created failed: expected number is: %d" %count )

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)
def bvtvolumecreateandlist(c,volnum):
    i=0
    j=0
    count=0
    FailFlag=False
    volnum=int(volnum)
    # tolog("I am here")
    pooldct=getpoolinfo(c)
    # administrator@cli> pool
    # ===============================================================================
    # Id    Name    Status    TotalCapacity    UsedCapacity    FreeCapacity
    # ===============================================================================
    # 1     11      OK        72.48 GB         69.63 KB        72.48 GB
    for poolid,poolvalue in pooldct.items():
        if (poolvalue[1]=="OK") or (poolvalue[1]=="OK, Synch") and float(poolvalue[-1].split(" ")[0])<=float(poolvalue[-3].split(" ")[0]):
            for i in range(1,volnum+1):
                volumecreate(c,poolid,"pool"+random_key(3)+poolid+"_"+str(i),"","","")
                # volumecreate(c, poolid, "pool" + poolid + "_" + str(i), "")
                count+=1
                # tolog("I am here2")
        j+=1
    res=SendCmd(c,"volume")
    # tolog("I am here 3")
    if i==0:
        tolog("No volume exists")
    else:
        if len(res.split("\r\n")) ==  count+ 5 and str(count-1) in res:
            tolog("Volumes are created succesfully.")
        else:
            FailFlag=True
            tolog("Volumes are created failed: expected number is: %d" %count )

    return FailFlag

def snapshotcreateandlist(c,snapshotnum):
    snapshotnum=int(snapshotnum)
    volumedct = getvolinfo(c)
    i=0
    FailFlag=False
# administrator@cli> volume
# ===============================================================================
# Id   Name                   PoolId TotalCap    UsedCap     Status     OpStatus
# ===============================================================================
# 0    pool0_1                0      947.78 TB   16.38 KB    Exported   OK
# 1    pool0_2                0      909.85 TB   16.38 KB    Exported   OK
# 2    pool0_3                0      311.15 TB   16.38 KB    Exported   OK
# 3    pool0_4                0      812.33 TB   16.38 KB    Exported   OK
# 4    pool0_5                0      726.68 TB   16.38 KB    Exported   OK
# 5    pool0_6                0      299.74 TB   16.38 KB    Exported   OK
# 6    pool0_7                0      247.41 TB   16.38 KB    Exported   OK
# 7    pool0_8                0      230.05 TB   16.38 KB    Exported   OK
# 8    pool0_9                0      37.74 TB    16.38 KB    Exported   OK
# 9    pool0_10               0      70.20 TB    16.38 KB    Exported   OK
    for volumeid,volumevalue in volumedct.items():
        if (volumevalue[-1]=="OK" or volumevalue[-1]=="OK, Sync") and volumevalue[-2]=="Exported":
                # and float(volumevalue[-2].split(" ")[0])<=float(volumevalue[-3].split(" ")[0]):
            for i in range(1,snapshotnum+1):
                # snapshotcreate(c,volumeid,"volume"+volumeid+"_"+str(i),"","","")
                snapshotcreate(c, volumeid, "vol" + volumeid + "_" + str(i))

    res=SendCmd(c,"snapshot")
    # because build 50 still has the problem RB-234122: cli "snapshot" can not get all snapshots listed
    # jusr commented this section to verify snapshots number
    volnum=len(getvolinfo(c))
    if i==0:
        tolog("no snapshot")
    else:
        if len(res.split("\r\n")) ==  volnum * i+ 5 and str(volnum * i-1) in res:
            tolog("Snapshots are created succesfully.")
        else:
            FailFlag=True
            tolog("Snapshots are created failed: expected number is: %d" %(volnum * i))
    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

def bvtsnapshotcreateandlist(c,snapshotnum):
    snapshotnum=int(snapshotnum)
    volumedct = getvolinfo(c)
    i=0
    FailFlag=False
# administrator@cli> volume
# ===============================================================================
# Id   Name                   PoolId TotalCap    UsedCap     Status     OpStatus
# ===============================================================================
# 0    pool0_1                0      947.78 TB   16.38 KB    Exported   OK
# 1    pool0_2                0      909.85 TB   16.38 KB    Exported   OK
# 2    pool0_3                0      311.15 TB   16.38 KB    Exported   OK
# 3    pool0_4                0      812.33 TB   16.38 KB    Exported   OK
# 4    pool0_5                0      726.68 TB   16.38 KB    Exported   OK
# 5    pool0_6                0      299.74 TB   16.38 KB    Exported   OK
# 6    pool0_7                0      247.41 TB   16.38 KB    Exported   OK
# 7    pool0_8                0      230.05 TB   16.38 KB    Exported   OK
# 8    pool0_9                0      37.74 TB    16.38 KB    Exported   OK
# 9    pool0_10               0      70.20 TB    16.38 KB    Exported   OK
    for volumeid,volumevalue in volumedct.items():
        if (volumevalue[-1]=="OK" or volumevalue[-1]=="OK, Sync") and volumevalue[-2]=="Exported":
                # and float(volumevalue[-2].split(" ")[0])<=float(volumevalue[-3].split(" ")[0]):
            for i in range(1,snapshotnum+1):
                # snapshotcreate(c,volumeid,"volume"+volumeid+"_"+str(i),"","","")
                snapshotcreate(c, volumeid, "vol" + volumeid + "_" + str(i))

    res=SendCmd(c,"snapshot")
    # because build 50 still has the problem RB-234122: cli "snapshot" can not get all snapshots listed
    # jusr commented this section to verify snapshots number
    volnum=len(getvolinfo(c))
    if i==0:
        tolog("no snapshot")
    else:
        if len(res.split("\r\n")) ==  volnum * i+ 5 and str(volnum * i-1) in res:
            tolog("Snapshots are created succesfully.")
        else:
            FailFlag=True
            tolog("Snapshots are created failed: expected number is: %d" %(volnum * i))

    return FailFlag

def snapshotcreate(c,volid,snapshotname):

    SendCmd(c,"snapshot -a add -t volume -d "+volid+ " -s \"name="+snapshotname+"\"")

def clonecreate(c,snapshotid,clonename):
    SendCmd(c, "clone -a add -d " + snapshotid + " -s \"name=" + clonename+"\"")

def clonecreateandlist(c,clonenum):
    clonenum=int(clonenum)
    i=0
    FailFlag=False
#     administrator@cli> snapshot
# ================================================================================
# Id    Name      PoolId Type        SourceId  UsedCapacity   Status
# ================================================================================
# 60    volume48_ 4      volume      48        0 Byte         Un-export
# 61    volume48_ 4      volume      48        0 Byte         Un-export
# 62    volume48_ 4      volume      48        0 Byte         Un-export
# 63    volume48_ 4      volume      48        0 Byte         Un-export
# 64    volume48_ 4      volume      48        0 Byte         Un-export
    snapshotdct=getsnapshotinfo(c)
    for snapshotid,snapshotvalue in snapshotdct.items():
        for i in range(1,clonenum+1):
            clonecreate(c,snapshotid,snapshotvalue[0]+random_key(3)+"_"+str(i))
    res=SendCmd(c,"clone")
    # volnum=len(getvolinfo(c))
    snapnum=len(getsnapshotinfo(c))
    if i==0:
        tolog("no clone")
    else:
        if len(res.split("\r\n")) ==  snapnum * clonenum+ 5 and str(snapnum * clonenum-1) in res:
            tolog("Clones are created succesfully.")
        else:
            FailFlag=True
            tolog("Clones are created failed: expected number is: %d" %(snapnum * clonenum ))

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)
def bvtclonecreateandlist(c,clonenum):
    clonenum=int(clonenum)
    i=0
    FailFlag=False
#     administrator@cli> snapshot
# ================================================================================
# Id    Name      PoolId Type        SourceId  UsedCapacity   Status
# ================================================================================
# 60    volume48_ 4      volume      48        0 Byte         Un-export
# 61    volume48_ 4      volume      48        0 Byte         Un-export
# 62    volume48_ 4      volume      48        0 Byte         Un-export
# 63    volume48_ 4      volume      48        0 Byte         Un-export
# 64    volume48_ 4      volume      48        0 Byte         Un-export
    snapshotdct=getsnapshotinfo(c)
    for snapshotid,snapshotvalue in snapshotdct.items():
        for i in range(1,clonenum+1):
            clonecreate(c,snapshotid,snapshotvalue[0]+random_key(3)+"_"+str(i))
    res=SendCmd(c,"clone")
    # volnum=len(getvolinfo(c))
    snapnum=len(getsnapshotinfo(c))
    if i==0:
        tolog("no clone")
    else:
        if len(res.split("\r\n")) ==  snapnum * clonenum+ 5 and str(snapnum * clonenum-1) in res:
            tolog("Clones are created succesfully.")
        else:
            FailFlag=True
            tolog("Clones are created failed: expected number is: %d" %(snapnum * clonenum ))

    return FailFlag

def poolmodify(c):
    SendCmd(c,"pool -a mod ")

def poolmodifyandlist(c):

    # the preconditions of this case are:
    # 1. one pool with raid 5 or raid 6
    # 2. several numbers of volumes are created under the pool
    # 3. several snapshots/clones are created under the volume
    # 4. pool modify name
    # 5. pool extend
    # 6. pool transfer
    # pool -a mod -i 1 -s "name=xxx"
    #
    # pool -a transfer -i 1
    #
    # pool -a del -i 3
    #
    # pool -a extend -i 1 -p 1,3,5~9
    FailFlag=False
    pooldct=getpoolinfo(c)
    for poolid,poolvalue in pooldct.items():
    # modify pool name
        if "OK" in poolvalue or "OK, Synch" in poolvalue or "OK, Sync" in poolvalue:

            modifiedpoolname=random_key(5)
            SendCmd(c,"pool -a mod -i "+poolid +" -s \"name="+modifiedpoolname+"\"")
        # verify modified name
            res=SendCmd(c,"pool -i "+poolid)
            if modifiedpoolname not in res:
                tolog(Failprompt+"modifying name to "+modifiedpoolname)
                FailFlag=True
        # pool extend
            pdhddsddlst=getavailpd(c)
            for pdlst in pdhddsddlst:
                if pdlst:
                    pdids=str(pdlst).replace("[","").replace("]","")
                    SendCmd(c,"pool -a extend -i "+poolid +" -p "+pdids.replace(" ",""))
            SendCmd(c,"phydrv")
            res=getpdlist(c)
            for key,value in res.items():
                if "Pool0" not in value:
                    FailFlag=True
                    break


    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)



def getctrlinfo(c):
# administrator@cli> ctrl
# ===============================================================================
# CtrlId        Alias        OperationalStatus        ReadinessStatus
# ===============================================================================
# 1             tests        OK                       Active
# 2             rt2          OK                       Active
#
# Controller 1 is Primary
    ctrldata=SendCmd(c,"ctrl")
    ctrldata = ctrldata.split("\r\n")
    ctrltab = ctrldata[2]
    primaryctrl=ctrldata[-2]
    ctrldata = ctrldata[4:-3]

    ctrldict = {}

    for ctrlinfo in ctrldata:
        if "Controller 1 is Primary" in primaryctrl:
            ctrldict[ctrlinfo[0:(ctrltab.find("Alias") - 1)].rstrip()] = (
                # ctrlinfo[ctrltab.find("Alias"):(ctrltab.find("OperationalStatus") - 1)].rstrip(),
                ctrlinfo[ctrltab.find("OperationalStatus"):(ctrltab.find("ReadinessStatus") - 1)].rstrip(),
                ctrlinfo[ctrltab.find("ReadinessStatus"):].rstrip(),"1")
        else:
            ctrldict[ctrlinfo[0:(ctrltab.find("Alias") - 1)].rstrip()] = (
                # ctrlinfo[ctrltab.find("Alias"):(ctrltab.find("OperationalStatus") - 1)].rstrip(),
                ctrlinfo[ctrltab.find("OperationalStatus"):(ctrltab.find("ReadinessStatus") - 1)].rstrip(),
                ctrlinfo[ctrltab.find("ReadinessStatus"):].rstrip(), "2")
    return ctrldict
def phydrvlist(c):
    res=SendCmd(c,"phydrv")
    if "Error" in res:
        tolog(Fail)
    else:
        tolog(Pass)
def poolforceclean(c):

    clonedelete(c)
    # cloneinfo=SendCmd(c,"clone")
    # while not "No clone found" in cloneinfo:
    #
    #     clonenum=int(cloneinfo.split("\r\n")[-2].split(" ")[0])
    #     for i in range(0,clonenum+1):
    #         SendCmd(c,"clone -a del -i "+str(i))
    #     cloneinfo=SendCmd(c,"clone")
    #
    snapshotdelete(c)
    # snapshotinfo = SendCmd(c, "snapshot")
    # while not "No snapshot exists" in snapshotinfo:
    #
    #     snapshotnum = int(snapshotinfo.split("\r\n")[-2].split(" ")[0])
    #     for i in range(0, snapshotnum + 1):
    #         SendCmd(c, "snapshot -a del -i " + str(i))
    #     snapshotinfo = SendCmd(c, "snapshot")
    #
    volumedel(c)
    # volinfo=SendCmd(c,"volume")
    # while not "No volume exists" in volinfo:
    #
    #     volnum=int(volinfo.split("\r\n")[-2].split(" ")[0])
    #     for i in range(0,volnum+1):
    #         SendCmd(c,"volume -a del -i "+str(i))
    #     volinfo=SendCmd(c,"volume")
    #
    pooldel(c)
    # poolinfo = SendCmd(c, "pool")
    # while not "No pool in the subsystem" in poolinfo:
    #
    #     poolnum = int(poolinfo.split("\r\n")[-2].split(" ")[0])
    #     for i in range(0, poolnum + 1):
    #         SendCmd(c, "pool -a del -i " + str(i))
    #     poolinfo = SendCmd(c, "pool")

    arraysinfo = SendCmd(c, "arrays")
    while "Alias" in arraysinfo:

        arraysnum = int(arraysinfo.split("\r\n")[-2].split(" ")[0])
        for i in range(0, arraysnum + 1):
            SendCmd(c, "arrays -a del -d " + str(i))
        arraysinfo = SendCmd(c, "arrays")
        if "Subsystem lock by other is present" in arraysinfo:
            time.sleep(5)
    spareinfo = SendCmd(c, "spare")
    while "Revertible" in spareinfo:
        sparenum = int(spareinfo.split("\r\n")[-2].split(" ")[0])
        for i in range(0, sparenum + 1):
            SendCmd(c, "spare -a del -i " + str(i))
        spareinfo = SendCmd(c, "spare")
    tolog(Pass)



def poolcreateverify(c):
    # stripelst = ("64kb", "128kb", "256kb", "512kb", "1mb", "64Kb", "64kB", "64KB", "128Kb", "128KB", "128kB", "256Kb",
    #              "256KB", "256kB", "512Kb", "512KB", "512kB", "1Mb", "1MB", "1mB")
    stripelst = ("64kb", "128kb", "256kb", "512kb", "1mb")
    # sectorlst = ["512b", "1kb", "2kb", "4kb","512B", "1Kb", "2Kb", "4Kb","1KB", "2KB", "4KB","1kB", "2kB", "4kB"]
    sectorlst = ("512b", "1kb", "2kb","4kb")
    raidlevel=("1","5","6")
    pdlist=getavailpd(c)
    i=j=0
    for hdtype in pdlist:
        if len(hdtype)>0:


            for stripe in stripelst:
                for sector in sectorlst:
                    for raid in raidlevel:
                        if raid=="1":
                            pdid=random.sample(hdtype,2)

                        elif raid=="5":
                            pdid = random.sample(hdtype,3)
                        else:
                            pdid = random.sample(hdtype, 4)
                        pdids=str(pdid).replace("[","").replace("]","").replace(" ","")
                        aliasname = random_key(4)+"_" + raid + "_" + stripe + "_" + sector
                        settings = "name=" + aliasname + ",raid=" + raid + ", stripe=" + stripe + ", sector=" + sector
                        res=SendCmd(c, "pool -a add -s " + "\"" + settings + "\"" + " -p " + pdids)
                        i += 1
                        if "Error" in res or "Fail" in res:
                            tolog(Failprompt+" creating "+aliasname+" with pd "+pdids)

                        else:
                            SendCmd(c,"pool -a del -i 0")
                            j+=1

    tolog("Created %s and deleted %s" % (str(i),str(j)))
    if i==j:
        tolog(Pass)
    else:
        tolog(Fail)

def poolcreateverifyoutputerror(c):
    # output error validation
    # raid 1 with 1 disks, 3 disks
    # raid 5 with 1,2 disks
    # raid 6 with 1,2,3 disks
    pdlist = getavailpd(c)
    results=list()
    Failflag=False
    for hdtype in pdlist:
        if hdtype:
            raid="1"
            tolog("Verify 1 disk and 3 disks Raid 1")
            disknum=(1,3)
            for eachnum in disknum:
                pdid= random.sample(hdtype, eachnum)
                pdids = str(pdid).replace("[", "").replace("]", "").replace(" ", "")
                aliasname = random_key(4) + "_raid_" + raid
                settings = "name=" + aliasname + ",raid=" + raid
                results.append(SendCmd(c,"pool -a add -s "+"\""+settings+ "\"" + " -p " + pdids))
                SendCmd(c,"pool -a del -i 0")
            raid="5"
            tolog("Verify 1 disk and 1 disks Raid 5")

            disknum=(1,2)
            for eachnum in disknum:
                pdid= random.sample(hdtype, eachnum)
                pdids = str(pdid).replace("[", "").replace("]", "").replace(" ", "")
                aliasname = random_key(4) + "_raid_" + raid
                settings = "name=" + aliasname + ",raid=" + raid
                results.append(SendCmd(c,"pool -a add -s "+"\""+settings+ "\"" + " -p " + pdids))
                SendCmd(c, "pool -a del -i 0")

            raid = "6"
            tolog("Verify 1 disk and 1 disks Raid 5")

            disknum = (1, 2,3)

            for eachnum in disknum:
                pdid = random.sample(hdtype, eachnum)
                pdids = str(pdid).replace("[", "").replace("]", "").replace(" ", "")
                aliasname = random_key(4) + "_raid_" + raid
                settings = "name=" + aliasname + ",raid=" + raid
                results.append(SendCmd(c, "pool -a add -s " + "\""+settings + "\"" + " -p " + pdids))
                SendCmd(c, "pool -a del -i 0")
            i=0
            for eachres in results:
                # print eachres
                if not(("Error" in eachres) or ("Fail" in eachres) or ("Invalid" in eachres)):
                    tolog(Failprompt+eachres)
                    Failflag = True
                    i+=1

            tolog("There are %s errors when validating output error." %str(i))
            invalidstriplist=("0kb", "2mb")
            invalidsectorlist=("0kb","8kb")
            invalidraildlevel=("0","10","50","60","100")
            stripelst = ("64kb", "128kb", "256kb", "512kb", "1mb")
            # sectorlst = ["512b", "1kb", "2kb", "4kb","512B", "1Kb", "2Kb", "4Kb","1KB", "2KB", "4KB","1kB", "2kB", "4kB"]
            sectorlst = ("512b", "1kb", "2kb", "4kb")
            raidlevellst = ("1", "5", "6")
            results1=list()
            for stripe in invalidstriplist:

                settings = "name=" + aliasname + ",raid=" + random.choice(raidlevellst) + ", stripe=" + stripe + ", sector=" + random.choice(sectorlst)
                results1.append(SendCmd(c, "pool -a add -s " + "\"" + settings + "\"" + " -p " + str(pdid).replace("[", "").replace("]", "").replace(" ", "")))
            for sector in invalidsectorlist:
                settings = "name=" + aliasname + ",raid=" + random.choice(
                    raidlevellst) + ", stripe=" + random.choice(stripelst) + ", sector=" + sector
                results1.append(SendCmd(c, "pool -a add -s " + "\"" + settings + "\"" + " -p " + str(pdid).replace("[", "").replace("]", "").replace(" ", "")))
            for raidlevel in invalidraildlevel:
                settings = "name=" + aliasname + ",raid=" + raidlevel + ", stripe=" + random.choice(stripelst) + ", sector=" + random.choice(sectorlst)
                results1.append(SendCmd(c, "pool -a add -s " + "\"" + settings + "\"" + " -p " + str(pdid).replace("[",
                                                                                                                  "").replace(
                    "]", "").replace(" ", "")))
            for eachres in results1:
                if not(("Error" in eachres) or ("Fail" in eachres) or ("Invalid" in eachres)):
                    tolog(Failprompt+eachres)
                    Failflag = True

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

def spareinfo(c):

# administrator@cli> spare
# ===============================================================================
# Id   Status   PdId   Capacity   Revertible   Type     DedicatedToPool
# ===============================================================================
# 1    OK       16     4 TB       Enabled      Global   []
#
# administrator@cli>

    sparedata = SendCmd(c, "spare")
    sparedata = sparedata.split("\r\n")
    sparetab = sparedata[2]
    sparedata = sparedata[4:-1]
    sparedict = {}
    for spareinfo in sparedata:
        sparedict[spareinfo[0:(sparetab.find("Status") - 1)].rstrip()] = (
            spareinfo[sparetab.find("Status"):(sparetab.find("PdId") - 1)].rstrip(),
            spareinfo[sparetab.find("PdId"):(sparetab.find("Capacity") - 1)].rstrip(),
            spareinfo[sparetab.find("Capacity"):(sparetab.find("Revertible") - 1)].rstrip(),
            spareinfo[sparetab.find("Revertible"):(sparetab.find("Type") - 1)].rstrip(),
            spareinfo[sparetab.find("Type"):(sparetab.find("DedicatedToPool") - 1)].rstrip())

    return sparedict

def pooldel(c):

    count = 0
    Failflag=False
    poolinfo = SendCmd(c, "pool")
    while not "No pool in the subsystem" in poolinfo:

        poolnum = int(poolinfo.split("\r\n")[-2].split(" ")[0])
        for i in range(0, poolnum + 1):
            SendCmd(c, "pool -a del -i " + str(i))

            count += 1


        if count>poolnum+1:
            tolog("Some pools cannot be deleted.")
            Failflag=True
            break
        poolinfo = SendCmd(c, "pool")

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
        tolog("Pools are deleted successfully.")

def volumedel(c):
    volinfo=SendCmd(c, "volume")
    count = 0
    Failflag=False
    while not "No volume exists" in volinfo:

        volnum=int(volinfo.split("\r\n")[-2].split(" ")[0])
        for i in range(0,volnum+1):
            SendCmd(c,"volume -a del -i "+str(i))
            count += 1

        if count>volnum+1:
            tolog("Some volumes cannot be deleted.")
            Failflag=True
            break
        volinfo = SendCmd(c, "volume")
    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
        tolog("Volumes are deleted successfully.")

def snapshotdelete(c):
    snapshotinfo=SendCmd(c, "snapshot")
    count=0
    Failflag = False
    while not "No snapshot exists" in snapshotinfo:

        snapshotnum = int(snapshotinfo.split("\r\n")[-2].split(" ")[0])
        for i in range(0, snapshotnum + 1):
            SendCmd(c, "snapshot -a del -i " + str(i))
            count+=1

        if count>snapshotnum+1:
            tolog("Some snapshots cannot be deleted.")
            Failflag=True
            break
        snapshotinfo = SendCmd(c, "snapshot")
    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
        tolog("Snapshots are deleted successfully.")



def clonedelete(c):
    cloneinfo = SendCmd(c, "clone")
    count=0
    Failflag=False
    while not "No clone found" in cloneinfo:

        clonenum = int(cloneinfo.split("\r\n")[-2].split(" ")[0])
        for i in range(0, clonenum + 1):
            SendCmd(c, "clone -a del -i " + str(i))
            count+=1

        if count>clonenum+1:
            tolog("Some clones cannot be deleted.")
            Failflag=True
            break
        cloneinfo = SendCmd(c, "clone")
    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
        tolog("Clone are deleted successfully.")

def sparedrvcreate(c,sparenum):
    sparenum=int(sparenum)
    pdhddssdlist=getavailpd(c)
    i = 0
    for pdid in pdhddssdlist[0]:

        if i<sparenum:
            SendCmd(c,"spare -a add -p "+str(pdid))
        i+=1

    SendCmd(c,"spare")

def bvtsparedrvcreate(c,sparenum):
    sparenum=int(sparenum)
    pdhddssdlist=getavailpd(c)
    i = 0
    FailFlag=False
    result=list()
    for pdid in pdhddssdlist[0]:

        if i<sparenum:
            result.append(SendCmd(c,"spare -a add -p "+str(pdid)))
        i+=1

    for res in result:
        if "Error" in res or "Invalid" in res:
            FailFalg=True

    res=SendCmd(c,"spare")
    if len(res.split("\r\n")) == sparenum + 5 and str(sparenum - 1) in res:
        tolog("Snapshots are created succesfully.")
    else:
        FailFlag = True
        tolog("Snapshots are created failed: expected number is: %d" % sparenum)

    return FailFlag

def bvtsparedelete(c):
    spareinfo = SendCmd(c, "spare")
    count=0
    Failflag=False
    # while "spare not found" not in spareinfo:
    #
    #     sparenum = int(spareinfo.split("\r\n")[-2].split(" ")[0])
    #     for i in range(0, sparenum + 1):
    #         SendCmd(c, "spare -a del -i " + str(i))
    #         count+=1
    #
    #     if count>sparenum+1:
    #         tolog("Some spare cannot be deleted.")
    #         Failflag=True
    #         break
    #     spareinfo = SendCmd(c, "spare")

    SendCmd(c, "spare -a del -i 0")
    SendCmd(c, "spare -a del -i 1")
    return Failflag

def bvtpooldel(c):

    count = 0
    Failflag=False
    poolinfo = SendCmd(c, "pool")
    while not "No pool in the subsystem" in poolinfo:

        poolnum = int(poolinfo.split("\r\n")[-2].split(" ")[0])
        for i in range(0, poolnum + 1):
            SendCmd(c, "pool -a del -i " + str(i))

            count += 1


        if count>poolnum+1:
            tolog("Some pools cannot be deleted.")
            Failflag=True
            break
        poolinfo = SendCmd(c, "pool")

    return Failflag

def bvtvolumedel(c):
    volinfo=SendCmd(c, "volume")
    count = 0
    Failflag=False
    while not "No volume exists" in volinfo:

        volnum=int(volinfo.split("\r\n")[-2].split(" ")[0])
        for i in range(0,volnum+1):
            SendCmd(c,"volume -a del -i "+str(i))
            count += 1

        if count>volnum+1:
            tolog("Some volumes cannot be deleted.")
            Failflag=True
            break
        volinfo = SendCmd(c, "volume")

    return Failflag

def bvtsnapshotdelete(c):
    snapshotinfo=SendCmd(c, "snapshot")
    count=0
    Failflag = False
    while not "No snapshot exists" in snapshotinfo:

        snapshotnum = int(snapshotinfo.split("\r\n")[-2].split(" ")[0])
        for i in range(0, snapshotnum + 1):
            SendCmd(c, "snapshot -a del -i " + str(i))
            count+=1

        if count>snapshotnum+1:
            tolog("Some snapshots cannot be deleted.")
            Failflag=True
            break
        snapshotinfo = SendCmd(c, "snapshot")

    return Failflag



def bvtclonedelete(c):
    cloneinfo = SendCmd(c, "clone")
    count=0
    Failflag=False
    while not "No clone found" in cloneinfo:

        clonenum = int(cloneinfo.split("\r\n")[-2].split(" ")[0])
        for i in range(0, clonenum + 1):
            SendCmd(c, "clone -a del -i " + str(i))
            count+=1

        if count>clonenum+1:
            tolog("Some clones cannot be deleted.")
            Failflag=True
            break
        cloneinfo = SendCmd(c, "clone")

    return Failflag

def infodictret(c, name,leading,tailing):

    if leading=="":leading=0
    if tailing=="": tailing=0
    result = SendCmd(c, name)

    infolist = list()
    data = list()
    data = result.split("\r\n")
    originaltab = data[2+leading]
    tabtmp = data[2+leading].split(" ")
    table = list()

    # the first column of the table will be the key in the dict
    for eachtab in tabtmp:
        if  eachtab!="":
            table.append(eachtab.rstrip())
    data = data[(4+leading):-(1+tailing)]
    lentab = len(table) - 2
    Outinfo = dict()

    for info in data:

        i = 0
        infolist = list()
        for i in range(lentab):
            #print originaltab.find(table[i + 2]), table[i + 1]
            infolist.append(info[originaltab.find(table[i + 1]):originaltab.find(table[i + 2])-1].rstrip())
            if i==lentab-1:
                infolist.append(info[originaltab.find(table[i + 2]):- 1].rstrip())

        Outinfo[info.split(" ")[0]] = infolist

    return Outinfo
def about(c):
    SendCmd(c,"about")
    tolog(Pass)
if __name__ == "__main__":

    start=time.clock()
    c,ssh=ssh_conn()

    if not c:
        raise ValueError

    # record the version number of this time
    #SendCmd(c,"about")
    #print infodictret("clone")
    pooldict=infodict("ctrl")
    print pooldict.getobject()
    # remove pool/volume/snapshot/clone if possible.
    #poolcleanup(c)
    # poolforceclean(c)

    # get avail pd without deleting any pool
    #getavailpd(c)

    #poolcreateandlist(c,0)
    # poolcreateandlist(c,poolnum)
    # 0 - create as many as pools according to current available pds
    # 1 - create 1 pool and try to keep available pds if possible
    # 2 - create 1 pool with all available pds

    # pool name is renamed and extend with other available disks
    #poolmodifyandlist(c)

    #volumecreateandlist(c, 20)
    # volumecreateandlist(c,volnum)
    # create 3 volumes for each pool

    #snapshotcreateandlist(c,20)
    # snapshotcreateandlist(c,snapshotnum)
    # create snapshotnum snapshots for each volume
    #SendCmd(c,"snapshot")
    #clonecreateandlist(c, 10)
    # clonecreateandlist(c,clonenum)
    # create clonenum for each snapshot

    #poolcreateverify(c)
    #verify pool create with all options
    # stripe/sector/raid level
    #poolcreateverifyoutputerror(c)
    #SendCmd(c,"swmgt -a mod -n cli -s \"rawinput=disable\"")
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped