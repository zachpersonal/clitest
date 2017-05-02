
import paramiko
import time
import string
from to_log import tolog

def SendCmd(cmdstr):
    server = '10.84.2.146'
    uname = 'administrator'
    pwd = 'password'
    data = ''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, username=uname, password=pwd)
    c = ssh.invoke_shell()
    doneflag = False
    while True:
        if c.recv_ready():
            resp=c.recv(9999)
            print resp
            #data+=resp
            data='administrator@cli> '
        else:
            continue
    # only @cli, send command to console to execute
        while resp.endswith('@cli> '):
            #print cmdstr
            if cmdstr.endswith('\n'):
                c.send(cmdstr)
            else:
                c.send(cmdstr+'\n')

            time.sleep(5)

            data+=c.recv(9999)
            tolog(data)
            for i in range(2):
             if "password for the new user" in data:
                c.send("123456\n")

            doneflag=True
            break

        if doneflag==True:
            break
    # print data
    ssh.close()
    #print data
    return data
