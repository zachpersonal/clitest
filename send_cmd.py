
import paramiko
import time
import string
from ssh_connect import check_ping
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
        # add code for password in user
            #print data
            #data=data.replace("[32D[32C[0m[?12l[?25h","").replace("[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m","")
            #print data

        while data.endswith('?25h'):
                #print data
                c.send("Local#123" + "\n")
                data += c.recv(2000)
                if data.endswith('@cli> '):
                    break
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

        # if data.endswith('?25h'):
        #     c.send("Local#123"+"\n")
    # data += c.recv(9999)


    data=data.replace("\x1b[D \x1b[D", "")
    data=data.replace("[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m","").replace("[32D[32C[0m[?12l[?25h","").replace("[?7h[0m[?12l[?25h[?2004l[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m","")
    tolog(data)
    
    return data


def SendCmdRestart(c, cmdstr):
    data = ''

    if cmdstr.endswith('\n'):
        c.send(cmdstr)
    else:
        c.send(cmdstr + '\n')
    # time.sleep(1)

    while not c.exit_status_ready():
    #while a[1].get_transport().is_active():
        a=check_ping()
        if a==0:
            if c.recv_ready():
                # removig the following chars to avoid
                # <Fault -32700: 'parse error. not well formed'> when
                # updating to testlink

                data += c.recv(2000)
                # add code for password in user
                # print data
                # data=data.replace("[32D[32C[0m[?12l[?25h","").replace("[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m","")
                #print data

            while data.endswith('?25h'):
                # print data
                c.send("Local#123" + "\n")
                data += c.recv(2000)
                if data.endswith('@cli> '):
                    break
            if data.endswith('@cli> '):
                break
        else:
            tolog("Network connection lost.")
            break

    # time.sleep(2)
    # removig the following chars to avoid
    # <Fault -32700: 'parse error. not well formed'> when
    # updating to testlink

    while c.recv_ready():
        data += c.recv(2000)

        if data.endswith('@cli> '):
            break

            # if data.endswith('?25h'):
            #     c.send("Local#123"+"\n")
    # data += c.recv(9999)


    data = data.replace("\x1b[D \x1b[D", "")
    data = data.replace("[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m", "").replace("[32D[32C[0m[?12l[?25h",
                                                                                   "").replace(
        "[?7h[0m[?12l[?25h[?2004l[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m", "")
    tolog(data)

    return data