
# initial version
# March 20, 2017

buildserverurl="http://192.168.208.5/release/hyperion_ds/daily/"
tftpserver="root@10.84.2.99:/work/tftpboot/"
serv = "MjExLjE1MC42NS44MQ=="
u = "amFja3kubGlAY24ucHJvbWlzZS5jb20="
p = "NzcwMjE0WHA="

import requests
from bs4 import BeautifulSoup

import os
import glob
import time
def getnewbuild():


    download=False
    # get the current build folder

    files=glob.glob("/work/tftpboot/d5k-multi*.ptif")
    tftpbuildnumber12=0
    tftpbuildnumber13 = 0
    tmp12=tmp13=0
    for file in files:
        try:
            if int(file[25:27])==12:
                tmp12=int(file[-7:-5])
            elif int(file[25:27]) == 13:
                tmp13 = int(file[-7:-5])
        except:
            tmp12=0
            tmp13=0
        if tmp12>tftpbuildnumber12:
           tftpbuildnumber12=tmp12
        if tmp13>tftpbuildnumber13:
           tftpbuildnumber13=tmp13

    # print "current build is %d" %tftpbuildnumber
    # to get the full directory list
    soup = BeautifulSoup(requests.get(buildserverurl).text)
    buildnumber12 = list()
    buildnumber13 = list()
    for link in soup.find_all('a'):
        tmp = link.get('href')
        if "13." in tmp:
            buildnumber13.append(tmp)
        if "12." in tmp:
            buildnumber12.append(tmp)


    try:

        webupdatedbuild12=int((buildnumber12[-1].replace("/","").split(".")[-1]))
        webupdatedbuild13 = int((buildnumber13[-1].replace("/", "").split(".")[-1]))
    except:
        webupdatedbuild12=0
        webupdatedbuild13 = 0

    print "webupdatedbuildnumbers are %d,%d" %(webupdatedbuild12,webupdatedbuild13)
#   if the webupdated build is newer than the installed one, download the new build
#   file list contains the filename to be updated on the host
    filelist=list()
    print "webupdatebuild12,tptpbuildnumber12",webupdatedbuild12,tftpbuildnumber12
    print "webupdatebuild13,tptpbuildnumber13", webupdatedbuild13, tftpbuildnumber13
    if webupdatedbuild13 >tftpbuildnumber13:
        download=True
        Pfile = open('downloadedfiles', 'w')
        Pfile.close()
        #for filetype in ("conf", "multi"):
        for filetype in ("conf", "multi", "bios", "fw", "lib", "oem", "sw", "usr", "base"):

            if filetype=="base":
                filename="d5k-"+filetype+"-"+(buildnumber13[-1].replace("/","")).replace(".","_").replace("13_00","13_0")+".raw.gz"

            else:
                filename="d5k-"+filetype+"-"+(buildnumber13[-1].replace("/","")).replace(".","_").replace("13_00","13_0")+".ptif"
            os.system("wget "+buildserverurl+buildnumber13[-1]+filename)
            # os.system("scp "+ filename +" "+tftpserver)
            # filename="d5k-"+filetype+"-"+webupdatedbuild.replace(".","_").replace("00","0")+".ptif"
            #
            #os.system("wget " + buildserverurl + buildnumber[-1] + "/" + filename)

            timestr=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            os.system("echo " + timestr +" downloaded %s" % filename +" >> downloadedfiles")
            os.system("mv /root/d5k* /work/tftpboot/")

            os.system("mv ./d5k* /work/tftpboot/")

    if webupdatedbuild12 > tftpbuildnumber12:
        download = True
        Pfile = open('downloadedfiles', 'w')
        Pfile.close()
        # for filetype in ("conf", "multi"):
        for filetype in ("conf", "multi", "bios", "fw", "lib", "oem", "sw", "usr", "base"):

            if filetype == "base":
                filename = "d5k-" + filetype + "-" + (buildnumber12[-1].replace("/", "")).replace(".", "_").replace(
                    "12_00", "12_0") + ".raw.gz"

            else:
                filename = "d5k-" + filetype + "-" + (buildnumber12[-1].replace("/", "")).replace(".", "_").replace(
                    "12_00", "12_0") + ".ptif"
            os.system("wget " + buildserverurl + buildnumber12[-1] + filename)
            # os.system("scp "+ filename +" "+tftpserver)
            # filename="d5k-"+filetype+"-"+webupdatedbuild.replace(".","_").replace("00","0")+".ptif"
            #
            # os.system("wget " + buildserverurl + buildnumber[-1] + "/" + filename)

            timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            os.system("echo " + timestr + " downloaded %s" % filename + " >> downloadedfiles")
            os.system("mv /root/d5k* /work/tftpboot/")

            os.system("mv ./d5k* /work/tftpboot/")

    return download

if __name__ == "__main__":

    timestr=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    os.system("echo %s \" Trying to download files\" >> downloadedfiles" %timestr )
    download=getnewbuild()
    if download==True:
        import smtplib

        # Import the email modules we'll need
        from email.mime.text import MIMEText

        # Open a plain text file for reading.  For this example, assume that
        # the text file contains only ASCII characters.
        textfile="downloadedfiles"
        fp = open(textfile, 'rb')
        buildversion=fp.readline()[-18:-6]
        tofile=open("buildnum","w")
        tofile.write(buildversion.replace("_","."))
        tofile.close()
        os.system("scp /root/buildnum root@192.168.252.106:/opt/testlink-1.9.16-0/apache2/htdocs/srvpool/")
        time.sleep(1)
        os.system("scp /root/buildnum root@10.84.2.66:/home/work/jackyl/")
        time.sleep(1)
        # Create a text/plain message
        msg = MIMEText(fp.read())
        fp.close()

        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = 'New build is available, please see the %s for detail' % textfile
        msg['From'] = 'jacky.li@cn.promise.com'
        msg['To'] = 'jacky.li@cn.promise.com'
        # Send the message via our own SMTP server, but don't include the
        #rec = ['ken.hou@cn.promise.com','xin.wang@cn.promise.com','lily.zhao@cn.promise.com','lisa.xu@cn.promise.com','jacky.li@cn.promise.com','hulda.zhao@cn.promise.com']
        rec = ['zach.feng@cn.promise.com','jacky.li@cn.promise.com','hulda.zhao@cn.promise.com']
        # Send the message via our own SMTP server, but don't include the
        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        u=u.decode('base64')
        serv=serv.decode('base64')
        p=p.decode('base64')


        s = smtplib.SMTP(serv)
        s.login(u,p)
        s.sendmail(msg['From'], rec, msg.as_string())
        s.quit()
