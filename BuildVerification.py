# initial version
# March 16, 2017
# architecture
# 1. getnewbuild from buildserver
# 2. scp to tftpserver
# 3. login to hypersion-DS console, execute
#    ptiflash -t -s 10.84.2.99 -f d5k-multi-12_0_9999_xx.ptif
#    ptiflash -t -s 10.84.2.99 -f d5k-conf-12_0_9999_48.ptif
# 4. execute auto script for cli and webgui
# 5. send email according to the test result

buildserverurl="http://192.168.208.5/release/hyperion_ds/daily/"
tftpserver="root@10.84.2.99:/work/tftpboot/"
import pool
from time import sleep

import os

from send_cmd import *
from ssh_connect import *
forBVT = True
from to_log import *

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def BuildVerification(c):
    Failflag=False
    flashimage=False
    c, ssh = ssh_conn()

    versioninfo = SendCmd(c, "about")

    currentbuild = versioninfo.split("Version: ")[1][:13]



    tftpbuildnumber=open("/home/work/jackyl/Scripts/clitest/buildnum","r").readline().rstrip()
    print currentbuild
    print tftpbuildnumber

    if ("13." in currentbuild and "13." in tftpbuildnumber) and (int(currentbuild.split(".")[-1])<int(tftpbuildnumber.split(".")[-1])) or (
        "12." in currentbuild and "12." in tftpbuildnumber) and (
        int(currentbuild.split(".")[-1]) < int(tftpbuildnumber.split(".")[-1])):
        #filename="d5k-multi-13_0_0000_"+tftpbuildnumber.split(".")[-1]
        if "13." in tftpbuildnumber:
            filename = "d5k-multi-13_0_0000_" + tftpbuildnumber.split(".")[-1]
        elif "12." in tftpbuildnumber:
            filename = "d5k-multi-12_0_9999_" + tftpbuildnumber.split(".")[-1]

        tolog("%s will be updated to the %s" % (filename, server))
        flashimage = True
        SendCmdRestart(c,"ptiflash -y -t -s 10.84.2.99 -f "+filename+".ptif")




    if flashimage:
        i=1
        while i< 260:
            # wait for rebooting
           tolog("ptiflash is in progress, please wait, %d seconds elapse" %i)
           i+=1
           sleep(1)

    # check if ssh connection is ok.
    # wait for another 40 seconds
        reconnectflag=False
        for x in range(10):
            try:
                c,ssh=ssh_conn()
                reconnectflag=True
            except Exception, e:
                print e
                sleep(4)


        if reconnectflag:
            tolog("Start verifying pool add")
            Failflag=pool.bvtpoolcreateandlist(c,1)

            tolog("Start verifying volume add")
            Failflag=pool.bvtvolumecreateandlist(c,10)

            tolog("Start verifying snapshot add")
            Failflag=pool.bvtsnapshotcreateandlist(c,2)

            tolog("Start verifying clone add")
            Failflag=pool.bvtclonecreateandlist(c,2)

            tolog("Start verifying spare add")
            Failflag = pool.bvtsparedrvcreate(c, 2)

            tolog("Start verifying delete clone")
            Failflag = pool.bvtclonedelete(c)

            tolog("Start verifying delete snapshot")
            Failflag = pool.bvtsnapshotdelete(c)

            tolog("Start verifying delete volume")
            Failflag = pool.bvtvolumedel(c)

            tolog("Start verifying delete pool")
            Failflag = pool.bvtpooldel(c)

            tolog("Start verifying delete spare")
            Failflag = pool.bvtsparedelete(c)


        else:
            tolog("Failed to connect server after ptiflash.")
            Failflag=True


        if Failflag:
            tolog(Fail)
        else:
            tolog(Pass)
    else:
        tolog("no new build is availlable.")
        tolog(Pass)

    c.close()
if __name__ == "__main__":

    start=time.clock()
    c,ssh=ssh_conn()
    BuildVerification(c)
    c.close()