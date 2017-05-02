
import paramiko
import time
import string
from ssh_connect import ssh_conn
from to_log import tolog


def SendCmd(c,cmdstr):
    data=''
    if cmdstr.endswith('\n'):
        c.send(cmdstr)
    else:
        c.send(cmdstr + '\n')
    # time.sleep(1)

    while not c.exit_status_ready():
        if c.recv_ready():

        # removig the following chars to avoid
        # <Fault -32700: 'parse error. not well formed'> when
        # updating to testlink

            data += c.recv(2000)
        if data.endswith('@cli> '):
            break
    # time.sleep(2)
    # removig the following chars to avoid
    # <Fault -32700: 'parse error. not well formed'> when
    # updating to testlink
    while c.recv_ready():
        data += c.recv(2000)
        if data.endswith('@cli> '):
            break

    # data += c.recv(9999)
    data=data.replace("\x1b[D \x1b[D", "")
    tolog(data)
    
    return data
if __name__ == "__main__":
    import sys
    c,ssh=ssh_conn()
    cmd = str(sys.argv[1])
    SendCmd(c,cmd)
    ssh.close()