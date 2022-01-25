import os
import getpass
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
os.system('/home/ansible/ansible-network/local_script/svn_up.bash')
print('Connection to devices')
open('/home/ansible/hp-conf/results/result_conf_timeout.txt', 'w').close()
open('/home/ansible/hp-conf/results/result_conf_auth_fail.txt', 'w').close()
open('/home/ansible/hp-conf/results/result_conf_ssh_fail.txt', 'w').close()
def job(IP1):
   IP2=[]
   IP2=IP1.split(' ')
   #cfg_file = '/home/ansible/ansible-network/playbooks/HP/config_files/test_config.txt'
   cfg_file = '/tmp/delete_sntp/'+IP2[0]+'.txt'
   DEVICE_PARAMS = {'device_type': 'hp_procurve',
                     'ip': str(IP2[1]),
                     'username': USER,
                     'password': PASSWORD}

   try:
    with ConnectHandler(**DEVICE_PARAMS) as ssh:
        ssh.enable()
        ssh.config_mode()
        output = ssh.send_config_from_file(cfg_file)
        write_m = ssh.send_command('write memory')
    print(bcolors.OKGREEN +"   ==  Successfully for device " + IP1 + "  ==" + bcolors.ENDC)	
    ssh.disconnect()
   except (NetMikoTimeoutException):
    print(bcolors.FAIL +"     !!!  Device timed out " + IP1 + "  !!!" + bcolors.ENDC)
    with open('/home/ansible/hp-conf/results/result_conf_timeout.txt','a') as result:
      result.write(" !!!  Device timed out " + IP1 + "  !!!\n")
   except (NetMikoAuthenticationException):
    print(bcolors.WARNING + "     !!!  Authentication failed for device " + IP1 + "  !!!" + bcolors.ENDC)
    with open('/home/ansible/hp-conf/results/result_conf_auth_fail.txt','a') as result:
      result.write(" !!!  Authentication failed for device " + IP1 + "  !!!\n")
   except (SSHException):
    print(bcolors.WARNING + "     !!!  SSH failed for device " + IP1 + "  !!!" + bcolors.ENDC)
    with open('/home/ansible/hp-conf/results/result_show_ssh_fail.txt','a') as result:
      result.write(" !!!  SSH failed for device " + IP1 + "  !!!\n")

def parallel_runs(IP1):
 pool = TreadPool(20)
 results = pool.map(job, IP1)
 pool.close()
 pool.join()
if __name__ == '__main__':
 USER = raw_input('Enter username: ')
 PASSWORD = getpass.getpass()
#COMMAND = raw_input('Enter command: ')
 IPLIST = '/home/ansible/ansible-network/HP_IP/Office-'+raw_input('Enter file inventory: ')+'.txt'
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
os.system('sh /home/ansible/ansible-network/local_script/svn_ci.bash')
# print (IP1)
