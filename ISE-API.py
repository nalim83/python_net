import requests
import json
import urllib3
import math

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def find_endpointgroup():
    group_id = {}
#    curl -k --header  'Accept: application/json' --user ****-api:******  https://10.106.78.46:9060/ers/config/endpointgroup?filter=name.EQ.Whitelist'
    uri = 'https://10.106.78.46:9060/ers/config/endpointgroup?'
    header = {"Accept":"application/json", "Authorization":"Basic *******"}
    res = requests.request(method='GET',url=uri,headers=header, verify=False)
    for i in res.json()['SearchResult']['resources']:
        group_id[i['name']] = i['id']
#    print(group_id)
    
    return group_id['Printers'], group_id['Avaya_Telephone']

def add_endpoint(MAC):
    uri = 'https://10.106.78.46:9060/ers/config/endpoint'
    header = {"Content-Type":"application/json", "Authorization":"Basic *****"}

    Data  = '{"ERSEndPoint" : {"name" : "Whitelisted_Endpoint",                       \
                               "description" : "Whitelisted Endpoint",                \
                               "mac" : "' +MAC+'",                                    \
                               "groupId" : "fd20fbb0-b463-11e9-a783-ee32eca97b4e",    \
                               "staticGroupAssignment" : true}}'
    res = requests.request(method='POST',url=uri,headers=header, data=Data,verify=False)
    print(res)

def find_endpoint(MAC):
    uri = 'https://10.106.78.46:9060/ers/config/endpoint?filter=mac.EQ.'+str(MAC)          #05:01:02:03:55:55'
    header = {"Accept":"application/json", "Authorization":"Basic ********"}
    res = requests.request(method='GET',url=uri,headers=header, verify=False)
    print(res.json())
    ID = res.json()['SearchResult']['resources'][0]['id']
#    print(ID)
    return ID


def delete_endpoint(MAC):
#    curl -k --include --header 'Accept: application/json' --user ****-api:*****  --request DELETE https://10.106.78.46:9060/ers/config/endpoint/fd20fbb0-b463-11e9-a783-ee32eca97b4e
    ID = find_endpoint(MAC)
    print(ID)
    uri = ' https://10.106.78.46:9060/ers/config/endpoint/'+str(ID)          #05:01:02:03:55:55'
    header = {"Accept":"application/json", "Authorization":"Basic *******"}
    res = requests.request(method='DELETE',url=uri,headers=header, verify=False)
    print(res)

def all_endpoint():
    MAC_ADR = {}
    p,a = find_endpointgroup()
    uri = 'https://10.106.78.46:9060/ers/config/endpoint?filter=groupId.EQ.'+p+'&size=100'
    header = {"Accept":"application/json", "Authorization":"Basic *********"}
    res = requests.request(method='GET',url=uri,headers=header, verify=False)
    total = res.json()['SearchResult']['total']
    page = math.ceil(int(total)/100)
    i = 1
    while i<=page:
        url = uri+'&page='+str(i)
        res = requests.request(method='GET',url=url,headers=header, verify=False)
        for k in res.json()['SearchResult']['resources']:
            mac_adr = k['name']
            id_ = k['id']
#            print('MAC :  ' + str(mac_adr) + ' , ' + 'ID :' + str(id_))
            MAC_ADR[k['name']] = k['id']
        i = i+1
    print(total)
    print(MAC_ADR)
  
if __name__ == '__main__':
    MAC = "05:01:02:03:55:55"
    all_endpoint()
#    find_endpoint(MAC)
#    delete_endpoint(MAC)
#    p,a = find_endpointgroup()
#    print(p)
#    print(a)




