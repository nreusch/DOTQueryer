# -*- coding: utf-8 -*- 
import json
import requests

def query_json():
    headers = {
        'Host': 'www.rejseplanen.dk',
        'Content-Length': '573',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Origin': 'http://www.rejseplanen.dk',
        'Referer': 'http://www.rejseplanen.dk/webapp/index.html?',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7,da;q=0.6',
        'Connection': 'close',
    }

    params = (
        ('rnd', '1580568694649'),
    )

    data = '{"id":"6hk82vfegqxtx4cc","ver":"1.24","lang":"dan","auth":{"type":"AID","aid":"j1sa92pcj72ksh0-web"},"client":{"id":"DK","type":"WEB","name":"rejseplanwebapp","l":"vs_webapp"},"formatted":false,"ext":"DK.10","svcReqL":[{"req":{"stbLoc":{"name":"Vibenshus Runddel St. (Lyngbyvej)","lid":"A=1@O=Vibenshus Runddel St. (Lyngbyvej)@X=12562902@Y=55706090@U=86@L=000001367@B=1@p=1580385689@","type":"S","crd":{"x":"12562902","y":"55706090"}},"jnyFltrL":[{"type":"PROD","mode":"INC","value":8191}],"type":"DEP","sort":"PT","maxJny":-1,"dur":60},"meth":"StationBoard","id":"1|1|"}]}'

    response = requests.post('http://www.rejseplanen.dk/bin/iphone.exe', headers=headers, params=params, data=data, verify=False)

    return str(response.content)


def parse_json(s):
    y = json.loads(s)
    jnyL = y["svcResL"][0]["res"]["jnyL"]
    retL = []

    for jny in jnyL:
        if "jid" in jny:
            # Not every journey seems to have a jid
            if jny["prodL"][0]["fIdx"] == 5 and jny["prodL"][0]["tIdx"] == 29:
                # 150S to Kokkedal
                timeString = str(jny["stbStop"]["dTimeS"])
                retL.append(("150S - K", timeString))
            elif jny["prodL"][0]["fIdx"] == 5 and jny["prodL"][0]["tIdx"] == 16:
                # 150S to Gl. Holte
                timeString = str(jny["stbStop"]["dTimeS"])
                retL.append(("150S - Gl", timeString))
            elif jny["prodL"][0]["fIdx"] == 4 and jny["prodL"][0]["tIdx"] == 14:
                # 15E to Sohuset, Forskerparken
                timeString = str(jny["stbStop"]["dTimeS"])
                retL.append(("15E", timeString))
    return retL

def print_journeys(l):
    for x in l:
        print("{}: {}:{}:{}".format(x[0], x[1][0:2], x[1][2:4], x[1][4:6]))


r = query_json()
p = parse_json(r)
print_journeys(p)