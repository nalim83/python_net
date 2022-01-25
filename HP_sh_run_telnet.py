#!/usr/bin/env python
import os
import getpass
import logging
import telnetlib
import time
import re
from multiprocessing.dummy import Pool as TreadPool
from functools import partial

class bcolors:
 WARNING = '\033[93m'
 OKGREEN = '\033[92m'
 FAIL = '\033[91m'
 ENDC = '\033[0m'
os.system('sh /home/ansnetwork/config/ansible-network/local_script/svn_up.bash')
print('Connection to devices')
open('/home/ansnetwork/config/hp-conf/results/result_show_timeout.txt', 'w').close()
open('/home/ansnetwork/config/hp-conf/results/result_show_auth_fail.txt', 'w').close()
open('/home/ansnetwork/config/hp-conf/results/result_show_ssh_fail.txt', 'w').close()
logging.getLogger('paramiko.transport').addHandler(logging.NullHandler())

def to_bytes(line):
    return f"{line}\n".encode("utf-8")


def job_telnet(IP1):
   USER = 'bot_hp'
   PASSWORD = 'bot_hp'
   COMMAND = ['sh run']
   IP2=[]
   IP2=IP1.split(' ')
   try:
    with telnetlib.Telnet(IP2[1], 23, 10) as telnet:
        time.sleep(1)
        telnet.write(to_bytes('\r\n'))
        time.sleep(3)
        telnet.write(to_bytes(USER))
        telnet.write(to_bytes(PASSWORD))
        index, m, output = telnet.expect([b">", b"#"])
        if index == 0:
#            telnet.write(b"enable\n")
            telnet.read_until(b"Password")
            telnet.read_until(b"#", timeout=5)
        telnet.write(b"terminal length 1000\n")
        telnet.read_until(b"#", timeout=5)
        time.sleep(3)
#        telnet.read_all()
        telnet.read_very_eager()

        result = {}

        for COMM in COMMAND:
#            print(COMM)
            telnet.write(to_bytes(COMM))
            output = telnet.read_until(b"2#", timeout=5).decode("utf-8")
            result[COMM] = output.replace("\n\r", "\n")
        if 'Running configuration' in str(result[COMM]):
           print(bcolors.OKGREEN +"   ==  Successfully for device " + IP1 + "  ==" + bcolors.ENDC)	
           with open('/home/ansnetwork/config/hp-conf/'+str(IP2[0])+'_'+str(IP2[1]) +'.cfg', 'w') as f:
               f.write(result[COMM])
   except (IOError, Exception) as err:
    print(bcolors.FAIL +"     !!!  Device timed out " + IP1 + "  !!!" + bcolors.ENDC)
    with open('/home/ansnetwork/config/hp-conf/results/result_show_timeout.txt','a') as result:
      result.write(" !!!  Device timed out " + IP1 + "  !!!\n")

def parallel_runs(IP1):
 pool = TreadPool(10)
 results = pool.map(job_telnet, IP1)
 pool.close()
 pool.join()
if __name__ == '__main__':
 USER = 'bot_hp'
 PASSWORD = 'bot_hp'
 COMMAND = 'sh run'
 #IPLIST = '/home/ansnetwork/config/ansible-network/HP_IP/'+raw_input('Enter file inventory: ')+'.txt'
 IPLIST = '/home/ansnetwork/config/ansible-network/HP_IP/Office-ALL.txt'
 iplist = open(IPLIST,'r')
# iplist = open('iplist.txt','r')
 IP = iplist.read().splitlines()
 iplist.close()
 i=0
 IP1 = []
 while i<len(IP):
  if IP[i][0] !="#":
   IP1.append(IP[i])
   i = i +1
  else:
   i = i + 1
 parallel_runs(IP1)
os.system('sh /home/ansnetwork/config/ansible-network/local_script/svn_ci.bash')
# print (IP1)
