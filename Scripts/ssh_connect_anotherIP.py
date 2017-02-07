
import paramiko
import time

def ssh_conn_anotherip(ip):


    uname = 'administrator'
    pwd = 'password'
    data = ''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=uname, password=pwd)
    c = ssh.invoke_shell()
    # doneflag = False
    time.sleep(5)
    resp=''
    if c.recv_ready():
        resp = c.recv(9999)

        # data+=resp
        data = 'administrator@cli> '

    # only @cli, send command to console to execute
    if resp.endswith('@cli> '):
        return c,ssh
