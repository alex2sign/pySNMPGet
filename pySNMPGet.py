# -*- coding: utf-8 -*-
from typing import Any

import socket
import random
import datetime
# import ydbf
from struct import pack, unpack
# from datetime import datetime as dt
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.rfc1902 import Integer, IpAddress, OctetString
import os.path

community = 'public'
ip_nabor = \
    {
        "192.168.0.117": "3260-Okt-Left",
        "192.168.0.118": "3260-Okt-Right",
        "192.168.5.116": "3260-Lenina-Left",
        "192.168.5.115": "3260-Lenina-Right",
        "192.168.4.118": "3260-Gol-Res",
        "192.168.3.117": "3260-Oksk-Res",
        "192.168.6.210": "Xerox-OK",
        "192.168.6.29": "Xerox_3025_Mng",
        "192.168.0.115": "HP-M401-30cab",
        "192.168.6.119": "2015-Buh",
        "192.168.6.120": "2015-A5",
        "192.168.5.117": "225-Len-Zav",
        "192.168.0.216": "2015-16cab"
    }

values = \
    {
        "1.3.6.1.2.1.1.5.0": "HostName",
        "1.3.6.1.2.1.43.5.1.1.17.1": "SerNumber",
        "1.3.6.1.2.1.43.10.2.1.4.1.1": "PageCountTotal",
        "1.3.6.1.2.1.43.11.1.1.9.1.1": "OstatokList",
        "1.3.6.1.2.1.43.11.1.1.8.1.1": "Emkost",
        "1.3.6.1.2.1.43.11.1.1.6.1.1": "Description",
        "1.3.6.1.2.1.43.11.1.1.8.1.2": "DrumAll",
        "1.3.6.1.2.1.43.11.1.1.9.1.2": "DrumTek"
    }

now_date_time = datetime.datetime.today()
dir = os.path.abspath(os.curdir)
fileout = dir + '\statnew.txt'
if os.path.exists(fileout):
    os.remove(fileout)
f = open(fileout, 'w')

generator = cmdgen.CommandGenerator()
comm_data = cmdgen.CommunityData('server', community, 0)  # 1 means version SNMP v2c, 0 means version SNMP v1
for ip in ip_nabor.keys():
    data_list = []
    transport = cmdgen.UdpTransportTarget((ip, 161))
    i = 0
    for value in values.keys():
        real_fun = getattr(generator, 'getCmd')
        varBinds: Any
        res = (errorIndication, errorStatus, errorIndex, varBinds) \
            = real_fun(comm_data, transport, value)

        if errorIndication is None or errorStatus is True:
            for varBind in varBinds:
                str1 = ' = '.join([x.prettyPrint() for x in varBind])
                position1 = str1.find('=')
                data_list.append(str1[position1 + 2:])
                # print(data_list[i])
                f.write(now_date_time.strftime("%m.%d.%Y") + '^' + \
                        now_date_time.strftime("%H:%M:%S") + '^' + \
                        ip + '^' + data_list[i] + '\n')
                i = i + 1
        else:
            # print(res)
            str2 = ''
            for numFor in range(0, len(res)):
                str2 = str2 + str(res[numFor])
            f.write(now_date_time.strftime("%m.%d.%Y") + '^' + \
                    now_date_time.strftime("%H:%M:%S") + '^' + \
                    ip + '^' + str2 + '\n')

f.close()
