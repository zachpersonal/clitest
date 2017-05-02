
import paramiko
import time
import os
server = '10.84.2.164'
uname = 'administrator'
pwd = 'password'

def check_ping():

    response = os.system("ping -c 1 " + server)
    # and then check the response...
    # if response == 0:
    #     pingstatus = "Network Active"
    # else:
    #     pingstatus = "Network Error"

    return response

def ssh_conn():

    #server = '10.84.2.100'

    data = ''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, username=uname, password=pwd)
    c = ssh.invoke_shell()

    c.setblocking(1)
    resp=b''
    Rawinput=False
    time.sleep(1)
    while (not c.exit_status_ready()) or (not Rawinput):
        time.sleep(1)
        resp = c.recv(2000)
        if resp.decode().endswith('@cli> '):
            break
    # if c.recv_ready():
    #     resp = c.recv(9999)

        # data+=resp
        data = 'administrator@cli> '

        # to accept rawinput=disable cli status
        # to rawinput=enable first
        # modified on April 14th, 2017
        if resp.decode().endswith("25h"):
            c.send("swmgt -a mod -n cli -s \"rawinput=enable\""+"\n")
            Rawinput=True
            ssh.close()
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(server, username=uname, password=pwd)
            c = ssh.invoke_shell()


    # only @cli, send command to console to execute

    if resp.decode().endswith('@cli> '):

        return c,ssh
