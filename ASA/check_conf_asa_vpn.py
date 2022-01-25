# -*- coding: utf-8 -*-
import logging
from multiprocessing.dummy import Pool as TreadPool
from functools import partial

class bcolors:
 WARNING = '\033[93m'
 OKGREEN = '\033[92m'
 FAIL = '\033[91m'
 ENDC = '\033[0m'

def job(IP1):
   IP2=[]
   IP2=IP1.split(' ')
   CA_TP='CA_TP'
   CA_TP2=IP2[2]
   VPN_TP='VPN_TP'
   VPN_TP2=IP2[3]
   
   open('/home/ansnetwork/config/ios/LAN+WAN/Need_Command/'+IP2[0]+'.txt', 'w').close()
   data = open('/home/ansnetwork/config/ios/LAN+WAN/'+str(IP2[0])+'.cfg', 'r')
   output = data.read()
   if 'asa-vpn3-' in IP2[0]:
      path = '/home/ansnetwork/config/ansible-network/playbooks/Cisco/Check_config/ASA/find_comm_vpn3/'
      file = '/home/ansnetwork/config/ansible-network/playbooks/Cisco/Check_config/ASA/find_command_vpn3.txt'
   else:
      path = '/home/ansnetwork/config/ansible-network/playbooks/Cisco/Check_config/ASA/find_comm/'
      file = '/home/ansnetwork/config/ansible-network/playbooks/Cisco/Check_config/ASA/find_command.txt'
   with open(file,'r') as com_list:
      print("\n     !!!  " + IP2[0] + "   !!!")
      for line in com_list:
           if CA_TP in line:
              line= line.replace(CA_TP, CA_TP2)
           if VPN_TP in line:
              line= line.replace(VPN_TP, VPN_TP2)
           if line[:-1] not in output:
                print(bcolors.FAIL +IP2[0]+' '+ line[:-1] + ' - NO' + bcolors.ENDC)
                with open('/home/ansnetwork/config/ios/LAN+WAN/Need_Command/'+IP2[0]+'.txt','a') as need_comm:
                   need_comm.write(line +'\n')

   for filename in os.listdir(path):
     data1 = open(path+filename, 'r')
     com_list2 = data1.read()
          
     if com_list2 in output:
           print(filename[:-4]+' OK')
     else:
           print(filename[:-4]+' NOT OK')
      data1.close()
   data.close()

def parallel_runs(IP1):
 pool = TreadPool(1)
 results = pool.map(job, IP1)
 pool.close()
 pool.join()
if __name__ == '__main__':
 iplist = open('/home/ansnetwork/config/ansible-network/playbooks/Cisco/Check_config/ASA/ASA_VPN.txt','r')
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
 for file in os.listdir('/home/ansnetwork/config/ios/LAN+WAN/Need_Command/'):
    size = os.path.getsize('/home/ansnetwork/config/ios/LAN+WAN/Need_Command/'+file)
    if size == 0:
       os.remove('/home/ansnetwork/config/ios/LAN+WAN/Need_Command/'+file)

