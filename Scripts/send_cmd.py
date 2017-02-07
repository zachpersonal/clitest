
import paramiko
import time
import string
from to_log import tolog


def SendCmd(c,cmdstr):
    data=''
    if cmdstr.endswith('\n'):
        c.send(cmdstr)
    else:
        c.send(cmdstr + '\n')

    time.sleep(2)
    # removig the following chars to avoid
    # <Fault -32700: 'parse error. not well formed'> when
    # updating to testlink

    data += c.recv(9999)
    data=data.replace("\x1b[D \x1b[D", "")
    tolog(data)
    
    return data
