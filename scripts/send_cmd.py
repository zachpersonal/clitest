
import paramiko
import time
import string
from to_log import tolog
from send_cmd import SendCmd

def SendCmd(c,cmdstr):
    data=''
    if cmdstr.endswith('\n'):
        c.send(cmdstr)
    else:
        c.send(cmdstr + '\n')

    time.sleep(5)

    data += c.recv(9999)
    tolog(data)
    
    return data
