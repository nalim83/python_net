#!/usr/bin/env python
import os
import logging
from netmiko import ConnectHandler
from multiprocessing.dummy import Pool as TreadPool
from functools import partial
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
from netmiko.ssh_exception import SSHException

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
def job(IP1):
   IP2=[]
   IP2=IP1.split(' ')
   DEVICE_PARAMS = {'device_type': 'hp_procurve',
                     'ip': str(IP2[1]),
                     'username': USER,
                     'password': PASSWORD}

   try:
    with ConnectHandler(**DEVICE_PARAMS) as ssh:
      #  ssh.enable()
        output = ssh.send_command('sh run')
    if 'Running configuration' in str(output):
        print(bcolors.OKGREEN +"   ==  Successfully for device " + IP1 + "  ==" + bcolors.ENDC)	
        with open('/home/ansnetwork/config/hp-conf/'+str(IP2[0])+'_'+str(IP2[1]) +'.cfg', 'w') as f:
            f.write(output)
    ssh.disconnect()
   except (NetMikoTimeoutException):
    print(bcolors.FAIL +"     !!!  Device timed out " + IP1 + "  !!!" + bcolors.ENDC)
    with open('/home/ansnetwork/config/hp-conf/results/result_show_timeout.txt','a') as result:
      result.write(" !!!  Device timed out " + IP1 + "  !!!\n")
   except (NetMikoAuthenticationException):
    print(bcolors.WARNING + "     !!!  Authentication failed for device " + IP1 + "  !!!" + bcolors.ENDC)
    with open('/home/ansnetwork/config/hp-conf/results/result_show_auth_fail.txt','a') as result:
      result.write(" !!!  Authentication failed for device " + IP1 + "  !!!\n")
   except (SSHException):
    print(bcolors.WARNING + "     !!!  SSH failed for device " + IP1 + "  !!!" + bcolors.ENDC)
    with open('/home/ansnetwork/config/hp-conf/results/result_show_ssh_fail.txt','a') as result:
      result.write(" !!!  SSH failed for device " + IP1 + "  !!!\n")
   except (IOError, Exception) as err:
    print(err)

def parallel_runs(IP1):
 pool = TreadPool(5)
 results = pool.map(job, IP1)
 pool.close()
 pool.join()
if __name__ == '__main__':
 USER = 'bot_hp'
 PASSWORD = 'bot_hp'
 COMMAND = 'sh run'
 #IPLIST = '/home/ansnetwork/config/ansible-network/HP_IP/'+raw_input('Enter file inventory: ')+'.txt'
 IPLIST = '/home/ansnetwork/config/ansible-network/HP_IP/Office-ALL.txt'
 iplist = open(IPLIST,'r')
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
