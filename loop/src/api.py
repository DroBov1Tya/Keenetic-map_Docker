import requests
from config import headers

def rewrite():
    r = requests.get(url="http://api:8000/keenetic/rewrite_all", headers=headers)
    return r

def set_device(devices):
    for item in devices:
        data = {
            "mac": item.get("mac"),
            "via": item.get("via"),
            "ip": item.get("ip"),
            "hostname": item.get("hostname"),
            "name": item.get("name"),
            "interface": item["interface"]["description"],
            "registered": item.get("registered"),
            "access": item.get("access"),
            "permit": item.get("permit"),
            "priority": item.get("priority"),
            "active": item.get("active"),
            "rxbytes": item.get("rxbytes"),
            "txbytes": item.get("txbytes"),
            "uptime": item.get("uptime"),
            "first_seen": item.get("first-seen"),
            "last_seen": item.get("last-seen"),
            "link": item.get("link"),
            "auto_negotiation": item.get("auto-negotiation"),
            "speed": item.get("speed"),
            "duplex": item.get("duplex"),
            "port": item.get("port")
        }
        r = requests.post(url="http://api:8000/keenetic/set_device", json=data, headers=headers)
    return