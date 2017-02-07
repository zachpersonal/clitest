# coding=utf-8
# initial work on 2016.12.31
# this section includes verify proper cmd/parameters/options and
# some other boundary or misspelled parameters/options
from  send_cmd import SendCmd
from to_log import tolog
import string
import json

# define the test result for testlink api
Pass = "'result': 'p'"
Fail = "'result': 'f'"
Failprompt="Failed on verifying "


def verifynetinfo(c):

    Failflag=False
    tolog("Get net info:")
    result = SendCmd(c,"net"),SendCmd(c, "net -v"),SendCmd(c,"net -a list"),SendCmd(c,"net -alist")
    for each in result:
        if not( "Error" not in each and "IPv4" in each and "IPv6" in each):
            Failflag=True
    if Failflag:
        tolog('Verify net info fail')
        tolog(Fail)
    else:
        tolog('Verify net info pass')
        tolog(Pass)


def verfiynethelp(c):
    checkResult = ''
    FailFlag = False
    tolog("Verify Net Help: ")
    result = SendCmd(c,'net -h'),SendCmd(c,'net -h123')

    for each in result:
        print each
        if not ('net' in each and 'Usage' in each and 'Summary' in each and 'to display info page by page' in each):
            FailFlag = True


    if FailFlag:
        tolog('Verify Net Help fail')
        tolog(Fail)
    else:
        tolog('Verify Net Help pass')
        tolog(Pass)

def enable_and_disable_ip_family(c):
    # if we disable the network we are currently connected with
    # the connection will be lost.
    # so, try to disable the network you are not using
    Failflag=False
    ipv4,ipv6= getnetinfo(c)

    # if "IPv4    Enabled" in origresult:
    #     result=SendCmd(c,"net -a disable -f ipv4")
    #     modifiedresult=SendCmd(c,"net -v")
    #     if not ("IPv4   Disabled" in modifiedresult):
    #         Failflag=True
    #         tolog(Failprompt+"net -a disable -f ipv4")
    # else:
    #     result = SendCmd(c, "net -a enable -f ipv4")
    #     modifiedresult = SendCmd(c, "net -v")
    #     if not ("IPv4   Enabled" in modifiedresult):
    #         Failflag = True
    #         tolog(Failprompt + "net -a enable -f ipv4")

    for i in range(2):
        print ipv6["ProtocolFamily"]
        if "Enabled" in ipv6["ProtocolFamily"]:
            result = SendCmd(c, "net -a disable -f ipv6")
            modifiedresult = SendCmd(c, "net -v")
            if not ("IPv6(Disabled)" in modifiedresult):
                Failflag = True
                tolog(Failprompt + "net -a disable -f ipv6")
        else:
            result = SendCmd(c, "net -a enable -f ipv6")
            modifiedresult = SendCmd(c, "net -v")
            if not ("IPv6(Enabled)" in modifiedresult):
                Failflag = True
                tolog(Failprompt + "net -a enable -f ipv6")
            ipv4, ipv6 = getnetinfo(c)

    # for some invalid parameters, IPv6, iPv6, ads, __
    for each in ("IPv6", "iPv6", "ads", "__"):
        result=SendCmd(c,'net -a enable -f '+each),SendCmd(c,'net -a disable -f '+each)
        for res in result:
            if not ("invalid protocol family" in res and "Error (0x402): Invalid parameter" in res):
                Failflag=True
                tolog(Failprompt+ res)

    if Failflag:
        tolog('Enable and Disable ip family fail')
        tolog(Fail)
    else:
        tolog('Enable and Disable ip family pass')
        tolog(Pass)

def getnetinfo(c):
    # the old hyperion net -v
    # ActiveCtrlId: 1                        Port: 1
    # MaxSupportedSpeed: 100Mbps             LinkStatus: Up
    #
    # ProtocolFamily: IPv4(Enabled)          DHCP: Disabled
    # IP: 10.84.2.146
    # IPMask: 255.255.255.0
    # DNS: 225.0.0.0
    # Gateway: 10.84.2.1
    # MAC: 00:01:55:59:EA:9D
    # WakeOnLAN: Enabled
    #
    # ProtocolFamily: IPv6(Enabled)          DHCP: Disabled
    # IP: 2017::1
    # IPMask: ffff::
    # DNS: 2017::3
    # Gateway: 2017::9
    # MAC: 00:01:55:59:EA:9D
    # WakeOnLAN: Enabled

    from ssh_connect import ssh_conn
    c, ssh = ssh_conn()
    import json

    a = SendCmd(c, "net -v")

    # a="ProtocolFamily: IPv4(Enabled)          DHCP: Disabled\nIP: 10.84.2.146\nIPMask: 255.255.255.0\nDNS: 225.0.0.0\nGateway: 10.84.2.1\nMAC: 00:01:55:59:EA:9D\nWakeOnLAN: Enabled\n"

    b = a.split("\r\n")
    for i in range(5):
        for item in b:
            if not (
                                    "ProtocolFamily" in item or "IP" in item or "DNS" in item or "Gateway" in item or "MAC" in item or "WakeOnLAN" in item):
                b.remove(item)

    net_v_ipv4_list = b[:7]
    net_v_ipv6_list = b[7:]

    #net_v_ipv4_list
    #print "v6 list", net_v_ipv6_list
    net_v_ipv4_dict = {}
    net_v_ipv6_dict = {}

    for each in net_v_ipv4_list:
        if "ProtocolFamily" in each:
            lista = each.split("          ")
            for eacha in lista:
                key = eacha.split(": ")[0]
                value = eacha.split(": ")[1]
                net_v_ipv4_dict[key] = value
        else:
            key = each.split(": ")[0]
            value = each.split(": ")[1]
            net_v_ipv4_dict[key] = value

    for each in net_v_ipv6_list:
        if "ProtocolFamily" in each:
            lista = each.split("         ")
            for eacha in lista:
                key = eacha.split(": ")[0]
                value = eacha.split(": ")[1]
                net_v_ipv6_dict[key] = value
        else:
            key = each.split(": ")[0]
            value = each.split(": ")[1]
            net_v_ipv6_dict[key] = value
    return net_v_ipv4_dict, net_v_ipv6_dict

    # the new hyperion DS net -v
    # -------------------------------------------------------------------------------
    # CtrlId: 2                               PortId: 1
    # MaxSupportedSpeed: 1000Mbps             Status: Up
    # WakeOnLAN: Disabled                     MAC: 00:01:55:5b:b2:5a
    # ===============================================================================
    # Family  Enable   DHCP      IP           IPMask         DNS      Gateway
    # ===============================================================================
    # IPv4    Enabled  Enabled   10.84.2.164  255.255.255.0  0.0.0.0  10.84.2
    # IPv6    Enabled  Disabled  2021::121   ffff::          ::       ::

def modifyandverifynetsettings(c):
    result = ""
    FailFlag = False
    origipv4,origipv6=getnetinfo(c)
    # change ip address
    # newip="10.84.2.145"
    # dns = "10.10.10.10"
    # gateway = "10.84.2.1"
    # mask = "255.255.255.0"
    # if origipv4["WakeOnLAN"] == "Enabled":
    #     wol = "disable"
    # else:
    #     wol = "enable"
    #
    # tolog("Modify and Verify net info:")
    # origresult=SendCmd(c, "net -v")
    # result = SendCmd(c,
    #                  "net -a mod -s \"primaryip=" + newip + ",primaryipmask=" + mask + ",primarydns=" + dns + ",gateway=" + gateway + ",wol=" + wol + "\"")
    # import time
    # time.sleep(2)
    # from ssh_connect_anotherIP import ssh_conn_anotherip
    # cnew, sshnew = ssh_conn_anotherip(newip)
    # #modipv4,modipv6=getnetinfo(cnew)
    # checkresult=SendCmd(cnew,"net -v")
    #
    # if not(origipv4["IP"] in origresult and newip in checkresult):
    #     FailFlag = True
    #     tolog(Failprompt + "modifying ipv4 adress.")
    # # change back to original ip address
    #
    # SendCmd(cnew, "net -a mod -s \"primaryip=" + origipv4['IP'] + ",primaryipmask=" + origipv4[
    #         'IPMask'] + ", primarydns=" + origipv4["DNS"] + ", gateway=" + origipv4["Gateway"] + ",wol=" + origipv4[
    #                 "WakeOnLAN"] + "\"")
    # SendCmd(cnew, "logout")
    # sshnew.close()
    #
    # if not ("" in result):
    #     FailFlag=True
    #     tolog(Failprompt+"sending change settings cmd.")
    # else:
    #     cnew,sshnew=ssh_conn_anotherip(newip)
    #     newipv4,newipv6=getnetinfo(cnew)
    #     if not(dns==newipv4['DNS'] and gateway==newipv4['Gateway'] and  mask==newipv4['IPMask']):
    #         FailFlag = True
    #         tolog(Failprompt+"changed settings are not correct")

    if "Disabled" in origipv6["ProtocolFamily"]:
        SendCmd(c,"net -a enable -f ipv6")

    newipv6 = "2017::2"
    dnsv6 = "2017::3"
    gatewayv6 = "2017::1"
    maskv6 = "ffff::"
    if origipv6["WakeOnLAN"] == "Enabled":
        wol = "disable"
    else:
        wol = "enable"

    tolog("Modify and Verify net info:")
    origresult=SendCmd(c, "net -v")
    p=", primarydns="
    result = SendCmd(c,
                     "net -a mod -f ipv6 -s \"primaryip=" + newipv6 + ", primaryipmask=" + maskv6 + p + dnsv6 + ", gateway=" + gatewayv6 + ", wol=" + wol + "\"")

    #modipv4,modipv6=getnetinfo(cnew)
    checkresult=SendCmd(c,"net -v")

    if not(newipv6 in checkresult and dnsv6 in checkresult and gatewayv6 in checkresult and maskv6 in checkresult):
        FailFlag = True
        tolog(Failprompt + "modifying ipv6 adress.")
    # change back to original ip address
    if origipv6["WakeOnLAN"]=="Enabled":
        wol='enable'
    else:
        wol="disable"

    SendCmd(c, "net -a mod -f ipv6 -s \"primaryip=" + origipv6['IP'] + ", primaryipmask=" + origipv6[
            'IPMask'] + p + origipv6["DNS"] + ", gateway=" + origipv6["Gateway"] + ", wol=" + wol + "\"")


    if not ("" in result):
        FailFlag=True
        tolog(Failprompt+"sending change settings cmd.")
    else:

        newipv4,newipv6=getnetinfo(c)
        if not(dnsv6==newipv4['DNS'] and gatewayv6==newipv4['Gateway'] and  maskv6==newipv4['IPMask']):
            FailFlag = True
            tolog(Failprompt+"changed settings are not correct")
    #SendCmd(cnew, "net -a mod -s \"primaryip=" + origipv4['IP'] + ",primaryipmask=" + origipv4['IPMask'] +", primarydns=" + origipv4["DNS"]+", gateway="+ origipv4["Gateway"]+",wol=" + origipv4["WakeOnLAN"] + "\"")


    if FailFlag:
        tolog('Verify modify and verify net info fail')
        tolog(Fail)
    else:
        tolog('Verify modify and verify net info pass')
        tolog(Pass)


def verifyyoption(c):
    # only letters, blank space and underscore are accepted
    # other chars are verified
    # no more than 48 char
    # leading spaces and tailing spaces are removed in the alias
    # length subsys alias = 48 chars
    # length controller alias = 48 chars
    # length array,ld alias =32 cahrs
    result1 = ""
    result2 =""
    FailFlag = False
    ipv4,ipv6=getnetinfo(c)
    if "Enabled" in ipv6["ProtocolFamily"]:
        result1=SendCmd(c,"net -a disable -f ipv6 -y")
    else:
        SendCmd(c,"net -a enable -f ipv6")
        result2=SendCmd(c, "net -a disable -f ipv6 -y")

    SendCmd(c,"net -a enable -f ipv6")

    result3=SendCmd(c,"net -a mod -f ipv6 -y -s \"primaryip=2017::12\"")

    if not ("" in result1 and "" in result2 and "" in result3):
        FailFlag=True
        tolog(Failprompt+"sending cmd with -y option.")
    if FailFlag:
        tolog('Modify subsys alias fail')
        tolog(Fail)
    else:
        tolog('Modify subsys alias pass')
        tolog(Pass)
def verifyMaintenancemode(c):
    # net -m
    # net -a mod -m -c 1 -f ipv6 -s "primaryip=2001::1"
    # net -a mod -m -c 1 -s "primaryip=10.84.2.145,wol=enable"
    # net -a enable -m -c 1 -f ipv6
    # net -m
    FailFlag=False
    origMresult=SendCmd(c,"net -m")
    ipv4,ipv6=getnetMinfo(c)
    if ipv6['IP']=="2001::1":
        ip="2001::2"
    else:
        ip="2001::1"

    cmd="net -a mod -m -c 1 -f ipv6 -s \"primaryip="+ ip +"\""
    result=SendCmd(c,cmd)
    if "Error" in result:
        FailFlag=True

    newMresult=SendCmd(c,"net -m")
    if ip not in newMresult:
        FailFlag=True
        tolog(Failprompt+"changing to maintenance ip addresd "+ip)

    if FailFlag:
        tolog('Verify modifing maintenance mode ip address failed')
        tolog(Fail)
    else:
        tolog('Verify modifing maintenance mode ip address passed')
        tolog(Pass)


def getnetMinfo(c):
    # the old hyperion net -v
    # ActiveCtrlId: 1                        Port: 1
    # MaxSupportedSpeed: 100Mbps             LinkStatus: Up
    #
    # ProtocolFamily: IPv4(Enabled)          DHCP: Disabled
    # IP: 10.84.2.146
    # IPMask: 255.255.255.0
    # DNS: 225.0.0.0
    # Gateway: 10.84.2.1
    # MAC: 00:01:55:59:EA:9D
    # WakeOnLAN: Enabled
    #
    # ProtocolFamily: IPv6(Enabled)          DHCP: Disabled
    # IP: 2017::1
    # IPMask: ffff::
    # DNS: 2017::3
    # Gateway: 2017::9
    # MAC: 00:01:55:59:EA:9D
    # WakeOnLAN: Enabled

    from ssh_connect import ssh_conn
    c, ssh = ssh_conn()
    import json

    a = SendCmd(c, "net -m")

#     -------------------------------------------------------------------------------
# CtrlId: 1                              Port: 1
# ProtocolFamily: IPv4(Enabled)          DHCP: Disabled
# IP: 10.0.0.3
# IPMask: 255.0.0.0
# DNS: 0.0.0.0
# Gateway: 0.0.0.0
# MAC: 00:01:55:59:EA:9D
#
# CtrlId: 1                              Port: 1
# ProtocolFamily: IPv6(Enabled)          DHCP: Disabled
# IP: 2001::1
# IPMask: ffff::
# DNS: ::
# Gateway: ::
# MAC: 00:01:55:59:EA:9D
#
#
# -------------------------------------------------------------------------------
# Controller 2 information not accessible
#

    b = a.split("\r\n")
    for i in range(5):
        for item in b:
            if not (
                                    "ProtocolFamily" in item or "IP" in item or "DNS" in item or "Gateway" in item or "MAC" in item):
                b.remove(item)

    net_m_ipv4_list = b[:7]
    net_m_ipv6_list = b[7:]

    #net_v_ipv4_list
    #print "v6 list", net_v_ipv6_list
    net_m_ipv4_dict = {}
    net_m_ipv6_dict = {}

    for each in net_m_ipv4_list:
        if "ProtocolFamily" in each:
            lista = each.split("          ")
            for eacha in lista:
                key = eacha.split(": ")[0]
                value = eacha.split(": ")[1]
                net_m_ipv4_dict[key] = value
        else:
            key = each.split(": ")[0]
            value = each.split(": ")[1]
            net_m_ipv4_dict[key] = value

    for each in net_m_ipv6_list:
        if "ProtocolFamily" in each:
            lista = each.split("         ")
            for eacha in lista:
                key = eacha.split(": ")[0]
                value = eacha.split(": ")[1]
                net_m_ipv6_dict[key] = value
        else:
            key = each.split(": ")[0]
            value = each.split(": ")[1]
            net_m_ipv6_dict[key] = value
    return net_m_ipv4_dict, net_m_ipv6_dict

    # the new hyperion DS net -v
    # -------------------------------------------------------------------------------
    # CtrlId: 2                               PortId: 1
    # MaxSupportedSpeed: 1000Mbps             Status: Up
    # WakeOnLAN: Disabled                     MAC: 00:01:55:5b:b2:5a
    # ===============================================================================
    # Family  Enable   DHCP      IP           IPMask         DNS      Gateway
    # ===============================================================================
    # IPv4    Enabled  Enabled   10.84.2.164  255.255.255.0  0.0.0.0  10.84.2
    # IPv6    Enabled  Disabled  2021::121   ffff::          ::       ::
