
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
    flashimage=False

    #c, ssh = ssh_conn()
    versioninfo = SendCmd(c, "about")

    currentbuild = versioninfo.split("Version: ")[1][:13]



    tftpbuildnumber=open("/home/work/jackyl/Scripts/buildnum","r").readline().rstrip()
    print int(tftpbuildnumber.split(".")[-1])
    if int(currentbuild.split(".")[-1])<=int(tftpbuildnumber.split(".")[-1]):
        filename="d5k-multi-12_0_9999_"+tftpbuildnumber.split(".")[-1]

        SendCmd(c,"ptiflash -y -t -s 10.84.2.99 -f "+filename+".ptif")

        tolog("%s will be updated to the %s" %(filename,server))
        flashimage=True


    if flashimage:
        i=1
        while i< 261:
            # wait for rebooting
           tolog("ptiflash is in progress, please wait, %d seconds elapse" %i)
           i+=1
           sleep(1)
    # check if ssh connection is ok.
    while not ssh.get_transport().is_active():
        c, ssh = ssh_conn()
        j=1
        while not ssh.get_transport().is_active():
            c, ssh = ssh_conn()
            print " ssh connection is in progress, please wait, %d seconds elapse" % j
            sleep(1)

        tolog("Start verifying pool add")
        pool.poolcreateandlist(c,0)
        tolog("Start verifying volume add")
        pool.volumecreateandlist(c,1025)
    else:
        tolog("no new build is availlable.")
        tolog(Pass)

    c.close()
if __name__ == "__main__":

    start=time.clock()
    c,ssh=ssh_conn()

    if not c:
        raise ValueError

    # record the version number of this time
    SendCmd(c,"about")
    BuildVerification(c)
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