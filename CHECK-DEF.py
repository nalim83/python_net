import sys
import fileinput

from datetime import datetime

open('/home/ansnetwork/config/ios/Default_on_ASR/Default_on_ASR.txt', 'w').close()

now = datetime.now()                              
DEVICES_F = ['asrx1.consultant.ru_def.cfg','asrx2.consultant.ru_def.cfg','asrx3.consultant.ru_def.cfg','asr.consultant.ru_def.cfg']
BGP = 'via "bgp'
EIGRP = 'via "eigrp'
STATIC = 'via "static"'
class bcolors:
 WARNING = '\033[93m'
 OKGREEN = '\033[92m'
 FAIL = '\033[91m'
 ENDC = '\033[0m'

for FILE in DEVICES_F:
      data = open('/tmp/'+FILE, 'r')
      output = data.read()
      if BGP in output:
              default = (FILE[:-8] + ' - Default from BGP')
              print(bcolors.OKGREEN +FILE[:-8] + ' - Default from BGP' + bcolors.ENDC)
              
      elif EIGRP in output:
              default = (FILE[:-8] + ' - Default from EIGRP')
              print(bcolors.WARNING +FILE[:-8] + ' - Default from EIGRP' + bcolors.ENDC)
              if ' 00:' in output:
                 print(bcolors.WARNING +FILE[:-8] + ' - Default from EIGRP'+'      !!! Achtung !!! Please check DEFAULT route ' + bcolors.ENDC)
                 print (output+"\n")
                 with open('/home/ansnetwork/config/ios/Default_on_ASR/Default_from_EIGRP.txt', 'a') as f:
                      f.write(str(now)[:-7] + '\n' + FILE[:-8] + ' - Default from EIGRP'+'      !!! Achtung !!! Please check DEFAULT route '+'\n'+'\n'+output+'\n'+'\n')
      elif STATIC in output: 
              default = (FILE[:-8] + ' - Default from STATIC ')
              if ' 00:' in output:
                 print(bcolors.FAIL +FILE[:-8] + ' - Default from STATIC ' + bcolors.ENDC)
                 print (output+"\n")
                 with open('/home/ansnetwork/config/ios/Default_on_ASR/Default_from_STATIC.txt', 'a') as f:
                      f.write(str(now)[:-7] + '\n' + FILE[:-8] + ' - Default from STATIC'+'     !!! Achtung !!! Please check DEFAULT route '+'\n'+'\n'+output+'\n'+'\n')

      with open('/home/ansnetwork/config/ios/Default_on_ASR/Default_on_ASR.txt', 'a') as f:
          f.write(default+'\n')
      data.close()


