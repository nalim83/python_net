import requests
import json
import urllib3
import os
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def find_prefix(net):
#    print(net)
    for i in net:
       if i == '8470':
         AS = 'Makomnet_AS8470'
       elif i == '8732':
         AS = 'Comkor_AS8732'
       elif i == '12389':
         AS = 'RT_AS12389'
       elif i == '47440':
         AS = 'BS-T_AS47440'
       elif i == '57724':
         AS = 'DDoS_AS57724'
       elif i == '20485':
         AS = 'TransTelekom_AS20485'
       print(AS)
       with open('/home/ansnetwork/config/ios/AS44014/'+AS, 'w') as f:
          f.write(AS + '\n')
          for k in net[i]:
             uri = 'https://api.radar.qrator.net/v1/paths/'+i+'?prefix='+k
             header = {"Accept":"application/json", "QRADAR-API-KEY":"*****"}
             z=0
             while z < 3:
                res = requests.request(method='GET',url=uri,headers=header, verify=False)
                a = res.json()
                if a['data'] is not None:
                   for x in a['data']:
                      l = str(a['data'][x])
                      print(x + " : " + l.replace("', '","'] ['"))
                      f.write(x + " : " + l.replace("', '","'] ['") + '\n')
                   time.sleep(1)
                   z = z+3
                else:
                   z = z+1
                   time.sleep(1)
                   if z == 3:
                      f.write(k +' : Not  data in Answer from api.radar.net after 3 retry' + '\n')
                
    return a


if __name__ == '__main__':
     os.system('/usr/bin/svn up /home/ansnetwork/config/ios/AS44014')
     net = {'8470':['194.105.130.0/24','194.105.131.0/24','194.105.130.0/23', '91.238.80.0/24','91.238.81.0/24','91.238.80.0/23'] , '8732':['194.105.130.0/24','194.105.131.0/24','194.105.130.0/23', '91.238.80.0/24','91.238.81.0/24','91.238.80.0/23'] , '12389':['194.105.130.0/24','194.105.131.0/24','194.105.130.0/23', '91.238.80.0/24','91.238.81.0/24','91.238.80.0/23'] , '47440':['194.105.130.0/24','194.105.131.0/24','194.105.130.0/23', '91.238.80.0/24','91.238.81.0/24','91.238.80.0/23'] , '57724':['194.105.130.0/24','194.105.131.0/24','194.105.130.0/23', '91.238.80.0/24','91.238.81.0/24','91.238.80.0/23'] , '20485':['194.105.130.0/24','194.105.131.0/24','194.105.130.0/23', '91.238.80.0/24','91.238.81.0/24','91.238.80.0/23']}
     find_prefix(net)
     os.system('sh /home/ansnetwork/config/ansible-network/local_script/svn_ci_as44014.bash')
