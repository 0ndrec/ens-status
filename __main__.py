from datetime import datetime
import requests
import json
import sys


time_now = datetime.now().timestamp()
time_now = int(time_now)

#104.18.11.19
url = "https://api.thegraph.com/subgraphs/name/ensdomains/ens" 
expirydate = time_now + 86400
id = sys.argv[1].lower()
domains = {}


if len(id) == 42 and id.startswith('0x'):
    pass
else:
    print("Invalid ID")
    sys.exit()


def to_date(timestamp):
    timestamp = int(timestamp)
    date = datetime.fromtimestamp(timestamp)
    return date.strftime("%Y-%m-%d")

with open("payload.json") as f:
    payload = json.load(f)


def get_name(url, payload, id, expirydate):
    try:
        payload["variables"]["id"] = id
        payload["variables"]["expiryDate"] = expirydate
        response = requests.post(url, json=payload)
        data = json.loads(response.text)
    except Exception as e: print(e)
    if data["data"]["account"] == None:
        print("No name found")
        sys.exit()
    registrations = data["data"]["account"]["registrations"]
    for registration in registrations:
        domains[registration["domain"]["name"]] = registration["expiryDate"]
    return domains

if __name__ == "__main__":
    get_name(url, payload, id, expirydate)
    for i in domains:
        days = (int(domains[i]) - time_now) / 86400
        print(i.upper(), ":  " , to_date(domains[i]), ":  ", int(days) , " days")